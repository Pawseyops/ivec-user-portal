-- Adds a group called privileges_reviewers and grants it add and change permission
-- to the review fields in the application form. Needed for that form to function properly.
BEGIN;

-- permissions are keyed to django content types
-- these are already present in production, but here's how it's done
--INSERT INTO django_content_type (name, applabel, model) VALUES ('reviewer score', 'allocation', 'reviewerscore');
--INSERT INTO django_content_type (name, applabel, model) VALUES ('reviewer comment', 'allocation', 'reviewercomment');

-- add the actual permission types
INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can add reviewer score', (SELECT id FROM django_content_type WHERE model='reviewerscore'), 'add_reviewerscore');
INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can change reviewer score', (SELECT id FROM django_content_type WHERE model='reviewerscore'), 'change_reviewerscore');
INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can delete reviewer score', (SELECT id FROM django_content_type WHERE model='reviewerscore'), 'delete_reviewerscore');
INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can add reviewer comment', (SELECT id FROM django_content_type WHERE model='reviewercomment'), 'add_reviewercomment');
INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can change reviewer comment', (SELECT id FROM django_content_type WHERE model='reviewercomment'), 'change_reviewercomment');
INSERT INTO auth_permission (name, content_type_id, codename)
    VALUES ('Can delete reviewer comment', (SELECT id FROM django_content_type WHERE model='reviewercomment'), 'delete_reviewercomment');

-- the rest of these are really fixtures that support the intended application workflow
INSERT INTO auth_group (name) VALUES ('privileged_reviewers');
INSERT INTO auth_group_permissions (group_id, permission_id) VALUES (
    (SELECT id FROM auth_group WHERE name='privileged_reviewers'),
    (SELECT id FROM auth_permission WHERE codename='add_reviewerscore')
);
INSERT INTO auth_group_permissions (group_id, permission_id) VALUES (
    (SELECT id FROM auth_group WHERE name='privileged_reviewers'),
    (SELECT id FROM auth_permission WHERE codename='change_reviewerscore')
);
INSERT INTO auth_group_permissions (group_id, permission_id) VALUES (
    (SELECT id FROM auth_group WHERE name='privileged_reviewers'),
    (SELECT id FROM auth_permission WHERE codename='add_reviewercomment')
);
INSERT INTO auth_group_permissions (group_id, permission_id) VALUES (
    (SELECT id FROM auth_group WHERE name='privileged_reviewers'),
    (SELECT id FROM auth_permission WHERE codename='change_reviewercomment')
);
COMMIT;
