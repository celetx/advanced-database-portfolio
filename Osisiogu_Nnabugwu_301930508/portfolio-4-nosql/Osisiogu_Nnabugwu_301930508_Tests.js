check(clinic.patients.countDocuments({})===5 && clinic.providers.countDocuments({})===3 &&
  clinic.services.countDocuments({})===5 && clinic.appointments.countDocuments({})===5 &&
  clinic.visits.countDocuments({})===5,'seed counts and CRUD cleanup');
check(JSON.stringify(results.revenueByMethod.map(x=>[x._id,x.totalKobo,x.paymentCount])) ===
  JSON.stringify([['Card',250000,1],['Cash',950000,2],['Transfer',1000000,2]]),'revenue by method: NGN 22,000 total');
check(JSON.stringify(results.serviceUtilisation.map(x=>[x._id,x.quantity,x.billedKobo])) ===
  JSON.stringify([[1,1,500000],[2,2,600000],[3,1,150000],[4,1,700000],[5,1,250000]]),'service quantities and historical billing');
check(results.patientHistory.length===1 && results.patientHistory[0].patient==='Ada Okeke' &&
  results.patientHistory[0].provider==='Dr. James Okoro','patient history lookup');
check(JSON.stringify(results.providerWorkload.map(x=>x.appointmentCount))==='[2,2,1]','provider workload including lookup');
rejected(()=>clinic.patients.insertOne(clinic.patients.findOne({_id:1})),11000,'duplicate primary key rejected');
rejected(()=>clinic.services.insertOne({_id:9001,name:'Invalid',feeKobo:-1,currency:'NGN'}),121,'negative fee rejected');
rejected(()=>clinic.services.insertOne({_id:9001,name:'General Consultation',feeKobo:1,currency:'NGN'}),11000,'duplicate service name rejected');
rejected(()=>clinic.patients.insertOne({_id:9001,fullName:null}),121,'missing and null patient fields rejected');
rejected(()=>clinic.appointments.updateOne({_id:1},{$set:{appointmentDate:'not a BSON date'}}),121,'invalid date type rejected');
rejected(()=>clinic.visits.updateOne({_id:1},{$set:{'services.0.quantity':0}}),121,'zero service quantity rejected');
rejected(()=>clinic.visits.updateOne({_id:1},{$set:{'payments.0.amountKobo':0}}),121,'zero payment rejected');
rejected(()=>clinic.appointments.updateOne({_id:1},{$set:{status:'Unknown'}}),121,'invalid appointment status rejected');
for (const name of ['appointments','visits']) {
  const orphans=clinic.getCollection(name).aggregate([
    {$lookup:{from:'patients',localField:'patientId',foreignField:'_id',as:'p'}},
    {$lookup:{from:'providers',localField:'providerId',foreignField:'_id',as:'r'}},
    {$match:{$or:[{p:{$size:0}},{r:{$size:0}}]}}
  ]).toArray();
  check(orphans.length===0,name+' references valid in seed data (application responsibility)');
}
check(clinic.visits.aggregate([{$unwind:'$services'},{$lookup:{from:'services',localField:'services.serviceId',foreignField:'_id',as:'s'}},
  {$match:{s:{$size:0}}}]).toArray().length===0,'embedded service references valid');
// A controlled counterexample: validators do not enforce foreign keys.
clinic.appointments.insertOne({_id:9002,patientId:9999,providerId:1,appointmentDate:new Date(),status:'Scheduled'});
check(clinic.appointments.findOne({_id:9002}).patientId===9999,'MongoDB accepts a syntactically valid orphan reference');
clinic.appointments.deleteOne({_id:9002});
const plan=clinic.appointments.find({patientId:1,appointmentDate:{$gte:ISODate('2026-11-01T00:00:00Z')}})
  .hint('patient_appointment_date').explain('executionStats');
show('Hinted compound index explain (demonstration, not a speed benchmark)',plan);
check(JSON.stringify(plan.queryPlanner.winningPlan).includes('IXSCAN'),'hinted compound index scan');
check(plan.executionStats.nReturned===1,'indexed query returns expected appointment');
print('ALL TESTS PASSED');
