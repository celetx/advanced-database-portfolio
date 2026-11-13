// Pipeline definitions are shared by the demonstration and result assertions.
const pipelines = {
 revenueByMethod:[{$unwind:'$payments'},{$match:{'payments.status':'Completed'}},
   {$group:{_id:'$payments.method',totalKobo:{$sum:'$payments.amountKobo'},paymentCount:{$sum:1}}},{$sort:{_id:1}}],
 serviceUtilisation:[{$unwind:'$services'},{$group:{_id:'$services.serviceId',
   quantity:{$sum:'$services.quantity'},billedKobo:{$sum:{$multiply:['$services.quantity','$services.unitFeeKobo']}}}},{$sort:{_id:1}}],
 patientHistory:[{$match:{patientId:1}},{$lookup:{from:'patients',localField:'patientId',foreignField:'_id',as:'patient'}},
   {$unwind:'$patient'},{$lookup:{from:'providers',localField:'providerId',foreignField:'_id',as:'provider'}},
   {$unwind:'$provider'},{$project:{_id:1,patient:'$patient.fullName',provider:'$provider.fullName',visitDate:1,status:1}},{$sort:{visitDate:-1}}],
 providerWorkload:[{$lookup:{from:'appointments',localField:'_id',foreignField:'providerId',as:'appointments'}},
   {$project:{_id:1,fullName:1,appointmentCount:{$size:'$appointments'}}},{$sort:{_id:1}}]
};
const results = {};
for (const [name,pipeline] of Object.entries(pipelines)) {
  results[name] = clinic.getCollection(name === 'providerWorkload' ? 'providers' : 'visits').aggregate(pipeline).toArray();
  show(name,results[name]);
}
