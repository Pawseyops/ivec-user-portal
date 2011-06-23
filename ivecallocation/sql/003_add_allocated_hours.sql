--- add if not already present
CREATE INDEX "allocation_reviewerscore_reviewer_id" ON "allocation_reviewerscore" ("reviewer_id");
CREATE INDEX "allocation_reviewercomment_reviewer_id" ON "allocation_reviewercomment" ("reviewer_id");


--- add new field
ALTER TABLE allocation_application ADD hours_allocated integer;