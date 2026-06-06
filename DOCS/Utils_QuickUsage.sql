SELECT * FROM public.student
ORDER BY id_student ASC 

/*ALTER TABLE public.student
ADD COLUMN course_timestamp TIMESTAMPTZ DEFAULT now();*/

UPDATE public.student AS ps
SET current_level = '2 - coccodrillo'
WHERE ps.id_student < 3

INSERT INTO student (name, surname, birth_date, current_level, goals, personal_notes, course_timestamp)
VALUES
('Alessandro', 'Giornimegi', '2022-01-01', 'A - stellina', 'B - granchietto', 'fluido coraggioso e carismatico, occhio al collo esplosivo', '11:45:00'),
('Alessio', 'Albia', '2022-01-01', 'A - stellina', 'B - granchietto', 'vertiginoso timidone che poi si scigolie', '11:45:00'),
('Afnan', 'Adnan', '2022-01-01', 'A - stellina', 'B - granchietto', 'dolci occhietti furbini con un sorrisone fantastico, sorellona di Yousef', '11:45:00'),
('Yousef', 'Adnan', '2023-01-01', 'A - stellina', 'B - granchietto', 'dolci occhietti furbini con una risatona fantastica, fratellino di Afnan', '11:45:00'),
('Giacomo', 'Reltopalpa', '2022-01-01', 'A - stellina', 'B - granchietto', 'indisponentino viziatino che vuole comandare, ha abbandonato la scialuppa a metà anno', '11:45:00'),
('Danilo', 'Vorticep', '2022-01-01', 'A - stellina', 'B - granchietto', 'pesciolino turbinoso fortissimo, mascotte del gruppo', '11:45:00'),
('Leon', '', '2021-01-01', 'A - stellina', 'B - granchietto', 'giappo-turbo coordinato, il più avanti', '11:45:00'),
('Davide', 'Montasio', '2021-01-01', 'A - stellina', 'B - granchietto', 'giappo-turbo coordinato, il più avanti', '11:45:00')
