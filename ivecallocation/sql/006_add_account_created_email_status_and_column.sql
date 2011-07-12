BEGIN;

INSERT INTO "allocation_participantstatus"("id", "name", "description") VALUES
    (5, 'Account Created Email Sent', 'The account creation notification email has been sent to the participant');

ALTER TABLE allocation_participant ADD COLUMN "account_created_email_on" timestamp with time zone;

COMMIT;

