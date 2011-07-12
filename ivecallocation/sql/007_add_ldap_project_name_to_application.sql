BEGIN;
ALTER TABLE "allocation_application" ADD COLUMN "ldap_project_name" varchar(256);
COMMIT;

