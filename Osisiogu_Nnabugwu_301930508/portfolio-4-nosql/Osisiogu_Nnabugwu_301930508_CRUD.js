// Temporary appointment; the fixture is unchanged after successful completion.
const temporary = {_id:9001,patientId:1,providerId:1,
  appointmentDate:ISODate('2026-11-20T09:00:00Z'),status:'Scheduled'};
check(clinic.appointments.insertOne(temporary).acknowledged, 'CREATE appointment 9001');
show('READ patient 1 appointments',clinic.appointments.find({patientId:1},{_id:1,status:1,appointmentDate:1}).sort({_id:1}).toArray());
check(clinic.appointments.findOne({_id:9001}).status === 'Scheduled','READ inserted appointment');
check(clinic.appointments.updateOne({_id:9001,status:'Scheduled'},{$set:{status:'Completed'}}).modifiedCount === 1,
  'UPDATE conditional status transition');
check(clinic.appointments.findOne({_id:9001}).status === 'Completed','READ updated status');
check(clinic.appointments.deleteOne({_id:9001}).deletedCount === 1,'DELETE temporary appointment');
check(clinic.appointments.countDocuments({_id:9001}) === 0,'READ confirms deletion');
