BEGIN;
UPDATE "allocation_institution" SET "ldap_ou_name"='University of Western Australia' WHERE "display_name" = 'University of Western Australia';
UPDATE "allocation_institution" SET "ldap_ou_name"='National' WHERE "display_name" = 'External';
COMMIT;

