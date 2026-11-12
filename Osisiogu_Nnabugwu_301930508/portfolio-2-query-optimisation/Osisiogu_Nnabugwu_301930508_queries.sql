
-- MIT 8103 Advanced Database Systems
-- Portfolio 2: Query Processing and Optimisation
-- Case Study: MediCare Health Clinic

-- Query 1: Retrieve patient appointments
SELECT
    p.FullName AS PatientName,
    pr.FullName AS ProviderName,
    a.AppointmentDate,
    a.Status
FROM Appointments a
JOIN Patients p ON a.PatientID = p.PatientID
JOIN Providers pr ON a.ProviderID = pr.ProviderID
ORDER BY a.AppointmentDate;


-- Query 2: Count appointments per provider
SELECT
    pr.FullName AS ProviderName,
    COUNT(a.AppointmentID) AS TotalAppointments
FROM Providers pr
LEFT JOIN Appointments a
    ON pr.ProviderID = a.ProviderID
GROUP BY pr.ProviderID, pr.FullName
ORDER BY TotalAppointments DESC;


-- Query 3: Calculate revenue by payment method
SELECT
    PaymentMethod,
    COUNT(*) AS TotalPayments,
    SUM(Amount) AS TotalRevenue
FROM Payments
WHERE PaymentStatus = 'Completed'
GROUP BY PaymentMethod
ORDER BY TotalRevenue DESC;


-- Query 4: Identify most frequently delivered services
SELECT
    ms.ServiceName,
    SUM(vs.Quantity) AS TotalServicesDelivered
FROM VisitServices vs
JOIN MedicalServices ms
    ON vs.ServiceID = ms.ServiceID
GROUP BY ms.ServiceID, ms.ServiceName
ORDER BY TotalServicesDelivered DESC;
