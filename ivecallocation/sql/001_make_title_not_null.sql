BEGIN;
UPDATE allocation_application SET project_title = '(untitled project)' WHERE project_title = '';
ALTER TABLE allocation_application ALTER COLUMN project_title SET NOT NULL;
END;

BEGIN;
ALTER TABLE allocation_researchfunding ALTER years TYPE varchar;
ALTER TABLE allocation_researchfunding ALTER total_funding TYPE varchar;
ALTER TABLE allocation_supportingfunding ALTER years TYPE varchar;
ALTER TABLE allocation_supportingfunding ALTER total_funding TYPE varchar;
COMMIT;
