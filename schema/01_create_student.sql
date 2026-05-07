CREATE TABLE IF NOT EXISTS student (
  id_student SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  surname VARCHAR(100) NOT NULL,
  birth_date DATE,
  current_level VARCHAR(50),
  goals TEXT,
  personal_notes TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_student_name_surname ON student(surname, name);

INSERT INTO student (name, surname, birth_date, current_level, goals, personal_notes)
VALUES
('Carlotta', 'Bonvicini', '1995-02-12', '2°/3°', '25SL breath focus + 25DO + RA upgrade', 'esperta GDO con chiacchera assiuda intra-vasca'),
('Andrea', 'Marcolongo', '1998-11-28', '2°/3°', '25SL breath focus + DO upgrade + RA upgrade', 'buon risponditore ai feedback')
