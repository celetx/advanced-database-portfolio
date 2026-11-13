// Reset only five named collections in an isolated teaching database.
const number = {bsonType: ['int', 'long', 'double'], minimum: 1, multipleOf: 1};
const text = {bsonType: 'string', minLength: 1};
const money = {bsonType: ['int', 'long', 'double'], minimum: 0, multipleOf: 1};
const positiveMoney = {...money, minimum: 1};
const dateType = {bsonType: 'date'};
const enumType = values => ({enum: values});
const object = (properties, required) => ({bsonType: 'object', required, properties});
const paymentSchema = object({paymentId: number, amountKobo: positiveMoney,
  method: enumType(['Cash','Transfer','Card']), status: enumType(['Pending','Completed','Failed']),
  paymentDate: dateType}, ['paymentId','amountKobo','method','status','paymentDate']);
const lineSchema = object({serviceId:number,name:text,unitFeeKobo:money,quantity:number},
  ['serviceId','name','unitFeeKobo','quantity']);
const definitions = {
 patients: object({_id:number,fullName:text,gender:text,phone:text,registrationDate:dateType,
   allergies:{bsonType:'array',items:text},schemaVersion:{enum:[1]}},
   ['_id','fullName','registrationDate','allergies','schemaVersion']),
 providers: object({_id:number,fullName:text,speciality:text},['_id','fullName','speciality']),
 services: object({_id:number,name:text,feeKobo:money,currency:{enum:['NGN']}},['_id','name','feeKobo','currency']),
 appointments: object({_id:number,patientId:number,providerId:number,appointmentDate:dateType,
   status:enumType(['Scheduled','Completed','Cancelled'])},['_id','patientId','providerId','appointmentDate','status']),
 visits: object({_id:number,patientId:number,providerId:number,visitDate:dateType,
   status:enumType(['Open','Completed','Cancelled']),services:{bsonType:'array',maxItems:100,items:lineSchema},
   payments:{bsonType:'array',maxItems:100,items:paymentSchema},clinicalNotes:{bsonType:'object'},schemaVersion:{enum:[1]}},
   ['_id','patientId','providerId','visitDate','status','services','payments','schemaVersion'])
};
for (const [name, schema] of Object.entries(definitions)) {
  clinic.getCollection(name).drop();
  clinic.createCollection(name, {validator:{$jsonSchema:schema},validationLevel:'strict',validationAction:'error'});
  clinic.getCollection(name).insertMany(readData(name[0].toUpperCase() + name.slice(1)));
}
clinic.services.createIndex({name:1},{unique:true,name:'unique_service_name'});
clinic.appointments.createIndex({patientId:1,appointmentDate:1},{name:'patient_appointment_date'});
clinic.appointments.createIndex({providerId:1,appointmentDate:1},{name:'provider_appointment_date'});
clinic.visits.createIndex({patientId:1,visitDate:-1},{name:'patient_visit_history'});
clinic.visits.createIndex({'services.serviceId':1},{name:'visit_services_multikey'});
show('Seed counts', Object.fromEntries(Object.keys(definitions).map(n => [n,clinic.getCollection(n).countDocuments({})])));
