-- Table: public.SUBJECTS

-- DROP TABLE IF EXISTS public."SUBJECTS";

CREATE TABLE IF NOT EXISTS public."SUBJECTS"
(
    "ID" uuid NOT NULL,
    "SUBJECT" character(50)[] COLLATE pg_catalog."default" NOT NULL,
    "TABLE_NAME" character(50)[] COLLATE pg_catalog."default" NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."SUBJECTS"
    OWNER to postgres;