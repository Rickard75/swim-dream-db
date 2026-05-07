ALTER TABLE student
    ADD CONSTRAINT uq_student UNIQUE (name, surname, birth_date);