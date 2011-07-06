BEGIN;



CREATE TABLE "allocation_participantstatus" (
    "id" INTEGER NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "description" varchar(256)
);

INSERT INTO "allocation_participantstatus"("id", "name", "description") VALUES 
    (1, 'New', 'Created as part of an application'),
    (2, 'Account Email Sent', 'An account creation email has been sent to the participant'),
    (3, 'Account Details Filled', 'The participant has filled in all the details needed to create the account'),
    (4, 'Account Created', 'The account has been created for the participant');

ALTER TABLE allocation_participant ADD COLUMN "status_id" INTEGER NOT NULL REFERENCES "allocation_participantstatus" ("id") DEFAULT 1;
ALTER TABLE allocation_participant ADD COLUMN "account_email_on" timestamp with time zone;
ALTER TABLE allocation_participant ADD COLUMN "account_email_hash" varchar(50);
ALTER TABLE allocation_participant ADD COLUMN "details_filled_on" timestamp with time zone;
ALTER TABLE allocation_participant ADD COLUMN "account_created_on" timestamp with time zone;

CREATE INDEX "allocation_participant_status_id" ON "allocation_participant" ("status_id");

COMMIT;

