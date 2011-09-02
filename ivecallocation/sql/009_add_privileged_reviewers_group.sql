-- Adds a group called privileges_reviewers and grants it add and change permission
-- to the review fields in the application form. Needed for that form to function properly.
BEGIN;
INSERT INTO auth_group (name) VALUES ('privileged_reviewers');
INSERT INTO auth_group_permission (group_id, permission_id) VALUES (
    SELECT id FROM auth_group WHERE name='privileged_reviewers',
    SELECT id FROM auth_permission WHERE codename='add_reviewerscore'
);
INSERT INTO auth_group_permission (group_id, permission_id) VALUES (
    SELECT id FROM auth_group WHERE name='privileged_reviewers',
    SELECT id FROM auth_permission WHERE codename='change_reviewerscore'
);
INSERT INTO auth_group_permission (group_id, permission_id) VALUES (
    SELECT id FROM auth_group WHERE name='privileged_reviewers',
    SELECT id FROM auth_permission WHERE codename='add_reviewercomment'
);
INSERT INTO auth_group_permission (group_id, permission_id) VALUES (
    SELECT id FROM auth_group WHERE name='privileged_reviewers',
    SELECT id FROM auth_permission WHERE codename='change_reviewercomment'
);
COMMIT;