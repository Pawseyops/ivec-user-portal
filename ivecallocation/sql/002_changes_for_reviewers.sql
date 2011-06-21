ALTER TABLE allocation_application ADD COLUMN "priority_area_directors" BOOLEAN NOT NULL DEFAULT 'f';
ALTER TABLE allocation_application ADD COLUMN "priority_area_partner" BOOLEAN NOT NULL DEFAULT 'f';
ALTER TABLE allocation_application ADD COLUMN "priority_area_national" BOOLEAN NOT NULL DEFAULT 'f';

CREATE TABLE "allocation_reviewerscore" (
    "id" serial NOT NULL PRIMARY KEY,
    "application_id" integer NOT NULL REFERENCES "allocation_application" ("id") DEFERRABLE INITIALLY DEFERRED,
    "research_merit" integer,
    "computational_merit" integer,
    "score" integer,
    "reviewer_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "allocation_reviewercomment" (
    "id" serial NOT NULL PRIMARY KEY,
    "application_id" integer NOT NULL REFERENCES "allocation_application" ("id") DEFERRABLE INITIALLY DEFERRED,
    "reviewer_comment" text,
    "reviewer_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
)
;



CREATE INDEX "allocation_reviewerscore_application_id" ON "allocation_reviewerscore" ("application_id");
CREATE INDEX "allocation_reviewercomment_application_id" ON "allocation_reviewercomment" ("application_id");


