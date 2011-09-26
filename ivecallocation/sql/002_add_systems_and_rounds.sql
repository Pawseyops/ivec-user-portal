BEGIN;

CREATE TABLE "allocation_system" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "description" varchar(1000) NOT NULL
);

INSERT INTO allocation_system (name, description) VALUES ('Epic', 'Epic Supercomputer at Murdoch University.');

CREATE TABLE "allocation_allocationround" (
    "id" serial NOT NULL PRIMARY KEY,
    "system_id" integer NOT NULL REFERENCES "allocation_system" ("id") DEFERRABLE INITIALLY DEFERRED,
    "start_date" date NOT NULL,
    "end_date" date NOT NULL,
    "name" varchar(512)
);

INSERT INTO allocation_allocationround (name, system_id, start_date, end_date) VALUES
    ('Epic legacy', (SELECT id from allocation_system where name='Epic'), '1970-01-01', '2011-09-01');
INSERT INTO allocation_allocationround (name, system_id, start_date, end_date) VALUES    
    ('Test open round', (SELECT id from allocation_system where name='Epic'), '2011-09-01', '2021-09-01');

ALTER TABLE "allocation_application" ADD COLUMN "allocation_round_id" integer;
UPDATE allocation_application SET allocation_round_id=(SELECT id from allocation_allocationround WHERE
    name='Epic legacy') ;
ALTER TABLE allocation_application ALTER COLUMN allocation_round_id SET NOT NULL;

ALTER TABLE "allocation_application" ADD CONSTRAINT allocation_allocation_round_id_fkey
    FOREIGN KEY (allocation_round_id) REFERENCES "allocation_allocationround" ("id") DEFERRABLE INITIALLY DEFERRED;

COMMIT;