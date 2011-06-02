BEGIN;
UPDATE allocation_application SET project_title = '(untitled project)' WHERE project_title IS NULL;
ALTER TABLE allocation_application ALTER COLUMN project_title SET NOT NULL;
END;

BEGIN;
ALTER TABLE allocation_researchfunding ALTER years MODIFY varchar;
ALTER TABLE allocation_researchfunding ALTER total_funding MODIFY varchar;
ALTER TABLE allocation_supportingfunding ALTER years MODIFY varchar;
ALTER TABLE allocation_supportingfunding ALTER total_funding MODIFY varchar;
COMMIT;