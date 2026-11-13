#!/usr/bin/env python3
"""PostgreSQL physical streaming replication lab; no Python third-party packages required."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import uuid

BASE = Path(__file__).resolve().parent
PREFIX = 'Osisiogu_Nnabugwu_301930508_'
IMAGE = 'postgres:16.11-bookworm'
ENV = os.environ.copy()
for variable in ('DOCKER_HOST', 'DOCKER_CONTEXT', 'DOCKER_TLS', 'DOCKER_TLS_VERIFY', 'DOCKER_CERT_PATH'):
    ENV.pop(variable, None)
DOCKER = ['docker', '--host=unix:///var/run/docker.sock']
TABLES = ['patients', 'providers', 'appointments', 'clinicvisits', 'medicalservices',
          'visitservices', 'payments', 'clinicbranches', 'clinicaccounts', 'distributionevents']


def command(args, emit=False, allow_error=False, timeout=90):
    result = subprocess.run(args, env=ENV, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=timeout)
    if emit and result.stdout:
        print(result.stdout.rstrip(), flush=True)
    if result.returncode and not allow_error:
        raise RuntimeError('Command failed (exit %s): %s' % (result.returncode, result.stdout))
    return result


def docker(*args, **kwargs):
    return command(DOCKER + list(args), **kwargs)


def check(ok, text):
    if not ok:
        raise AssertionError(text)
    print('PASS: ' + text, flush=True)


def heading(text):
    print('\n=== ' + text + ' ===', flush=True)


class Lab:
    def __init__(self):
        self.container = 'medicare-pg5-' + uuid.uuid4().hex[:12]
        self.started = False
        self.checks = []
        self.metrics = {}
        self.stage = 'startup'

    def __enter__(self):
        docker('run', '-d', '--name', self.container, '--network', 'none', IMAGE, 'sleep', 'infinity')
        self.started = True
        docker('cp', str(BASE) + '/.', self.container + ':/portfolio')
        docker('exec', self.container, 'chmod', '-R', 'a+rX', '/portfolio')
        return self

    def __exit__(self, error_type, error, trace):
        if error_type:
            print('FAILED DURING: ' + self.stage, flush=True)
            for name in ('primary', 'standby', 'rejoined'):
                docker('exec', self.container, 'tail', '-n', '12', '/tmp/' + name + '.log',
                       emit=True, allow_error=True)
        if self.started:
            result = docker('rm', '-fv', self.container, allow_error=True)
            if result.returncode:
                print('Cleanup warning: ' + result.stdout, flush=True)

    def pg(self, *args, **kwargs):
        return docker('exec', '-u', 'postgres', self.container, *args, **kwargs)

    def sql(self, port, sql, database='medicare_portfolio5', emit=False, allow_error=False):
        return self.pg('psql', '-X', '-h', '127.0.0.1', '-p', str(port), '-U', 'postgres',
                       '-d', database, '-v', 'ON_ERROR_STOP=1', '-v', 'VERBOSITY=verbose',
                       '-At', '-c', sql, emit=emit, allow_error=allow_error).stdout.strip()

    def sql_file(self, port, name):
        self.pg('psql', '-X', '-h', '127.0.0.1', '-p', str(port), '-U', 'postgres',
                '-d', 'medicare_portfolio5', '-v', 'ON_ERROR_STOP=1',
                '-f', '/portfolio/' + PREFIX + name + '.sql', emit=True)

    def start(self, directory, port, log):
        self.pg('pg_ctl', '-D', '/tmp/' + directory, '-l', '/tmp/' + log + '.log',
                '-o', '-p %s -k /tmp' % port, '-w', '-t', '30', 'start', emit=True)

    def stop(self, directory, mode='fast'):
        self.pg('pg_ctl', '-D', '/tmp/' + directory, '-m', mode, '-w', '-t', '30', 'stop', emit=True)

    def clone(self, source_port, target, slot):
        self.pg('pg_basebackup', '-h', '127.0.0.1', '-p', str(source_port), '-U', 'portfolio_replicator',
                '-D', '/tmp/' + target, '-R', '-X', 'stream', '-C', '-S', slot, '--checkpoint=fast', emit=True)

    def replay_barrier(self, primary, standby, key):
        lsn = self.sql(primary, 'SELECT pg_current_wal_lsn()')
        if not re.fullmatch(r'[0-9A-F]+/[0-9A-F]+', lsn):
            raise RuntimeError('Unexpected WAL LSN: ' + lsn)
        start = time.monotonic()
        deadline = start + 30
        while time.monotonic() < deadline:
            if self.sql(standby, "SELECT pg_last_wal_replay_lsn() >= '%s'::pg_lsn" % lsn) == 't':
                elapsed = round((time.monotonic() - start) * 1000, 3)
                self.metrics[key] = {'target_lsn': lsn, 'client_observed_wait_ms': elapsed}
                print('MEASURED: %s target=%s replay-catch-up-wait=%.3f ms (includes client/poll overhead)' %
                      (key, lsn, elapsed), flush=True)
                return
            time.sleep(0.1)
        raise RuntimeError('Replica did not replay target LSN within 30 seconds')

    def equality(self, primary, standby, label):
        digests = {}
        for table in TABLES:
            query = "SELECT md5(COALESCE(string_agg(row_to_json(t)::text, E'\\n' ORDER BY row_to_json(t)::text),'')) FROM %s t" % table
            first, second = self.sql(primary, query), self.sql(standby, query)
            if first != second:
                raise AssertionError('Content mismatch in ' + table)
            digests[table] = first
        print('Exact sorted-row content digests: ' + json.dumps(digests, sort_keys=True), flush=True)
        check(True, label + ': content matches across all ten tables')

    def replication_status(self, port):
        self.sql(port, "SELECT application_name, state, sync_state, sent_lsn, write_lsn, flush_lsn, replay_lsn, "
                 "pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS pending_bytes, replay_lag "
                 "FROM pg_stat_replication ORDER BY application_name", emit=True)

    def run(self):
        self.stage = 'SETUP AND CONNECTIONS'
        heading(self.stage)
        self.pg('initdb', '-D', '/tmp/primary', '--no-locale', '--encoding=UTF8',
                '--auth-local=trust', '--auth-host=reject')
        docker('exec', self.container, 'cp', '/portfolio/' + PREFIX + 'Primary.conf', '/tmp/primary/postgresql.conf')
        docker('exec', self.container, 'cp', '/portfolio/' + PREFIX + 'PgHba.conf', '/tmp/primary/pg_hba.conf')
        docker('exec', self.container, 'chown', 'postgres:postgres', '/tmp/primary/postgresql.conf', '/tmp/primary/pg_hba.conf')
        self.start('primary', 55432, 'primary')
        self.sql(55432, 'CREATE ROLE portfolio_replicator WITH LOGIN REPLICATION', 'postgres')
        self.pg('createdb', '-h', '127.0.0.1', '-p', '55432', 'medicare_portfolio5')
        for name in ('Schema', 'SampleData', 'Setup'):
            self.sql_file(55432, name)
        check(self.sql(55432, 'SELECT NOT pg_is_in_recovery()') == 't', 'initial node is writable primary')
        check(self.sql(55432, 'SELECT COUNT(*) FROM Patients') == '5', 'five fictional patients loaded')
        check(self.sql(55432, "SELECT SUM(Amount) FROM Payments WHERE PaymentStatus='Completed'") == '22000.00',
              'completed payment revenue is NGN 22,000')
        self.clone(55432, 'standby', 'medicare_branch_slot')
        self.start('standby', 55433, 'standby')
        check(self.sql(55433, 'SELECT pg_is_in_recovery()') == 't', 'remote-clinic node is a physical standby')
        self.replay_barrier(55432, 55433, 'initial_sync')
        check(self.sql(55432, "SELECT COUNT(*) FROM pg_stat_replication WHERE state='streaming' AND sync_state='async'") == '1',
              'WAL streaming connection is asynchronous')
        check(self.sql(55432, "SELECT active FROM pg_replication_slots WHERE slot_name='medicare_branch_slot'") == 't',
              'physical replication slot is active')
        self.replication_status(55432)
        self.sql_file(55433, 'Queries')
        self.equality(55432, 55433, 'initial primary/standby consistency')

        self.stage = 'REPLICATED INSERTS, UPDATES AND TRANSACTIONS'
        heading(self.stage)
        self.sql_file(55432, 'ReplicatedChanges')
        self.replay_barrier(55432, 55433, 'insert_update')
        check(self.sql(55433, "SELECT COUNT(*) FROM DistributionEvents WHERE EventKey='replicated-insert'") == '1',
              'insert reaches remote-clinic standby')
        check(self.sql(55433, 'SELECT Phone FROM Patients WHERE PatientID=1') == '08000000999',
              'patient update reaches remote-clinic standby')
        self.sql_file(55432, 'Transaction')
        self.replay_barrier(55432, 55433, 'committed_transfer')
        check(self.sql(55433, "SELECT string_agg(Balance::text,',' ORDER BY AccountID) FROM ClinicAccounts") == '90000.00,60000.00',
              'committed account transfer replays with expected balances')
        check(self.sql(55433, 'SELECT SUM(Balance) FROM ClinicAccounts') == '150000.00',
              'replica preserves NGN 150,000 account total')
        self.sql(55432, 'BEGIN; UPDATE ClinicAccounts SET Balance=Balance-20000 WHERE AccountID=1; '
                 'UPDATE ClinicAccounts SET Balance=Balance+20000 WHERE AccountID=2; ROLLBACK;')
        self.replay_barrier(55432, 55433, 'rolled_back_transfer')
        check(self.sql(55433, "SELECT string_agg(Balance::text,',' ORDER BY AccountID) FROM ClinicAccounts") == '90000.00,60000.00',
              'rolled-back transfer is absent from visible standby balances')
        rejected = self.pg('psql', '-X', '-h', '127.0.0.1', '-p', '55433', '-d', 'medicare_portfolio5',
                           '-v', 'ON_ERROR_STOP=1', '-v', 'VERBOSITY=verbose', '-c',
                           "INSERT INTO DistributionEvents VALUES ('standby-write',1,'must be rejected')",
                           allow_error=True, emit=True)
        check(rejected.returncode != 0 and '25006' in rejected.stdout, 'standby rejects writes with SQLSTATE 25006')
        self.equality(55432, 55433, 'after insert/update/transaction')

        self.stage = 'STANDBY INTERRUPTION AND CATCH-UP'
        heading(self.stage)
        self.stop('standby')
        self.sql(55432, "INSERT INTO DistributionEvents VALUES ('while-standby-down',3,'accepted by asynchronous primary')")
        check(self.sql(55432, "SELECT COUNT(*) FROM DistributionEvents WHERE EventKey='while-standby-down'") == '1',
              'primary acknowledges write while asynchronous standby is stopped')
        check(self.sql(55432, 'SELECT COUNT(*) FROM pg_stat_replication') == '0', 'no active WAL sender after standby stops')
        self.start('standby', 55433, 'standby')
        self.replay_barrier(55432, 55433, 'restart_catchup')
        check(self.sql(55433, "SELECT COUNT(*) FROM DistributionEvents WHERE EventKey='while-standby-down'") == '1',
              'restarted standby catches up from retained WAL')
        self.replication_status(55432)
        self.equality(55432, 55433, 'after standby recovery')

        self.stage = 'PRIMARY FAILURE, READ AVAILABILITY AND MANUAL PROMOTION'
        heading(self.stage)
        self.replay_barrier(55432, 55433, 'before_primary_failure')
        started = time.monotonic()
        self.stop('primary', mode='immediate')
        status = self.pg('pg_ctl', '-D', '/tmp/primary', 'status', allow_error=True)
        check(status.returncode == 3, 'old primary is stopped before promotion (lab fencing)')
        check(self.sql(55433, 'SELECT COUNT(*) FROM Patients') == '5', 'standby serves existing reads while primary is unavailable')
        self.pg('pg_ctl', '-D', '/tmp/standby', '-w', '-t', '30', 'promote', emit=True)
        self.metrics['manual_promotion'] = {'client_observed_elapsed_ms': round((time.monotonic()-started)*1000, 3),
                                             'scope': 'stop + checks + manual promotion; not an automated failover SLA'}
        check(self.sql(55433, 'SELECT NOT pg_is_in_recovery()') == 't', 'promoted standby becomes a writable primary')
        self.sql(55433, "INSERT INTO DistributionEvents VALUES ('after-promotion',2,'write on new timeline')")
        check(self.sql(55433, "SELECT COUNT(*) FROM DistributionEvents WHERE EventKey='after-promotion'") == '1',
              'new primary accepts post-promotion write')
        check(self.sql(55433, "SELECT string_agg(Balance::text,',' ORDER BY AccountID) FROM ClinicAccounts") == '90000.00,60000.00',
              'pre-failure account balances survive controlled promotion')

        self.stage = 'FORMER PRIMARY REJOINS FROM A NEW BASE BACKUP'
        heading(self.stage)
        # Never restart the old primary directory; create a fresh standby from the new timeline.
        self.clone(55433, 'rejoined', 'medicare_rejoin_slot')
        self.start('rejoined', 55432, 'rejoined')
        check(self.sql(55432, 'SELECT pg_is_in_recovery()') == 't', 'former primary endpoint now runs a fresh standby')
        self.replay_barrier(55433, 55432, 'rejoin_sync')
        check(self.sql(55432, "SELECT COUNT(*) FROM DistributionEvents WHERE EventKey='after-promotion'") == '1',
              'rejoined standby contains new-primary timeline write')
        self.equality(55433, 55432, 'after rejoin')
        self.replication_status(55433)

        self.stage = 'LOGICAL BACKUP AND RESTORE VALIDATION'
        heading(self.stage)
        archive = '/tmp/' + PREFIX + 'Backup.dump'
        self.pg('pg_dump', '-h', '127.0.0.1', '-p', '55433', '-Fc', '-f', archive, 'medicare_portfolio5')
        self.pg('createdb', '-h', '127.0.0.1', '-p', '55433', 'medicare_portfolio5_restore')
        self.pg('pg_restore', '-h', '127.0.0.1', '-p', '55433', '--exit-on-error',
                '-d', 'medicare_portfolio5_restore', archive)
        for table in TABLES:
            query = "SELECT md5(COALESCE(string_agg(row_to_json(t)::text, E'\\n' ORDER BY row_to_json(t)::text),'')) FROM %s t" % table
            check(self.sql(55433, query) == self.sql(55433, query, database='medicare_portfolio5_restore'),
                  'restored content matches: ' + table)
        check(self.sql(55433, 'SELECT SUM(Balance) FROM ClinicAccounts', database='medicare_portfolio5_restore') == '150000.00',
              'restored account total is NGN 150,000')
        print('MEASUREMENTS_JSON: ' + json.dumps(self.metrics, sort_keys=True), flush=True)


if __name__ == '__main__':
    print('MediCare Portfolio 5 PostgreSQL | ' + datetime.datetime.now(datetime.timezone.utc).isoformat(), flush=True)
    docker('info', '--format', 'Docker server: {{.ServerVersion}}', emit=True)
    docker('image', 'inspect', IMAGE, '--format', 'PostgreSQL image: {{index .RepoDigests 0}}', emit=True)
    with Lab() as lab:
        lab.pg('postgres', '--version', emit=True)
        lab.run()
    print('\nALL PORTFOLIO 5 TESTS PASSED', flush=True)
