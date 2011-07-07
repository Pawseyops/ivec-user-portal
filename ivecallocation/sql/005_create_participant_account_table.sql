BEGIN;

CREATE TABLE "allocation_institution" (
    "id" serial NOT NULL PRIMARY KEY,
    "display_name" varchar(256) NOT NULL,
    "ldap_ou_name" varchar(256) NOT NULL
);


CREATE TABLE "allocation_participantaccount" (
    "id" serial NOT NULL PRIMARY KEY,
    "participant_id" integer NOT NULL UNIQUE REFERENCES "allocation_participant" ("id") DEFERRABLE INITIALLY DEFERRED,
    "institution_id" integer REFERENCES "allocation_institution" ("id") DEFERRABLE INITIALLY DEFERRED,
    "first_name" varchar(256) NOT NULL,
    "last_name" varchar(256) NOT NULL,
    "phone" varchar(50),
    "uid" varchar(256),
    "uid_number" integer,
    "gid_number" integer,
    "password_hash" varchar(256),
    "ivec_terms_accepted" boolean NOT NULL,
    "old_ldap_details" varchar(2000),
    "data_fetched_on" timestamp with time zone NOT NULL
); 

COMMIT;

