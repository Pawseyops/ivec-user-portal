--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET search_path = public, pg_catalog;

--
-- Name: allocation_application_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_application_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: allocation_application; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_application (
    id serial,
    project_title character varying(100) NOT NULL,
    project_summary character varying(1000),
    priority_area_radio_astronomy boolean NOT NULL,
    priority_area_geosciences boolean NOT NULL,
    research_record character varying(5000),
    research_significance character varying(5000),
    computational_methodology character varying(5000),
    core_hours_requested integer,
    storage_temporary character varying(32),
    storage_resident character varying(32),
    storage_pbstore character varying(32),
    data_transfers character varying(512),
    created_by_id integer,
    created_on timestamp with time zone NOT NULL,
    complete boolean NOT NULL,
    priority_area_directors boolean DEFAULT false NOT NULL,
    priority_area_partner boolean DEFAULT false NOT NULL,
    priority_area_national boolean DEFAULT false NOT NULL,
    hours_allocated integer,
    ldap_project_name character varying(256)
);
SELECT pg_catalog.setval('allocation_application_id_seq', 104, true);

--
-- Name: allocation_fieldofresearchcode_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE allocation_fieldofresearchcode_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: allocation_fieldofresearchcode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_fieldofresearchcode; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_fieldofresearchcode (
    id serial,
    code integer,
    description character varying(256)
);
SELECT pg_catalog.setval('allocation_fieldofresearchcode_id_seq', 1, false);

--
-- Name: allocation_institution_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_institution_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_institution; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_institution (
    id serial,
    display_name character varying(256) NOT NULL,
    ldap_ou_name character varying(256) NOT NULL
);
SELECT pg_catalog.setval('allocation_institution_id_seq', 7, true);

--
-- Name: allocation_library_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_library_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_library; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_library (
    id serial,
    application_id integer NOT NULL,
    description character varying(256),
    reference character varying(256),
    licensing character varying(256)
);
SELECT pg_catalog.setval('allocation_library_id_seq', 321, true);

--
-- Name: allocation_participant_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_participant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_participant; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_participant (
    id serial,
    application_id integer NOT NULL,
    name character varying(256),
    department_institute character varying(128),
    email character varying(75),
    account boolean NOT NULL,
    "admin" boolean NOT NULL,
    student boolean NOT NULL,
    eft double precision,
    status_id integer DEFAULT 1 NOT NULL,
    account_email_on timestamp with time zone,
    account_email_hash character varying(50),
    details_filled_on timestamp with time zone,
    account_created_on timestamp with time zone,
    account_created_email_on timestamp with time zone
);
SELECT pg_catalog.setval('allocation_participant_id_seq', 276, true);

--
-- Name: allocation_participantaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_participantaccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_participantaccount; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_participantaccount (
    id serial,
    participant_id integer NOT NULL,
    institution_id integer,
    first_name character varying(256) NOT NULL,
    last_name character varying(256) NOT NULL,
    phone character varying(50),
    uid character varying(256),
    uid_number integer,
    gid_number integer,
    password_hash character varying(256),
    old_ldap_details character varying(2000),
    data_fetched_on timestamp with time zone
);
SELECT pg_catalog.setval('allocation_participantaccount_id_seq', 26, true);

--
-- Name: allocation_participantstatus; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_participantstatus (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(256)
);


--
-- Name: allocation_publication_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_publication_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_publication; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_publication (
    id serial,
    application_id integer NOT NULL,
    reference character varying(256),
    description character varying(256)
);
SELECT pg_catalog.setval('allocation_publication_id_seq', 523, true);

--
-- Name: allocation_researchclassification_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_researchclassification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_researchclassification; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_researchclassification (
    id serial,
    application_id integer NOT NULL,
    code integer,
    percentage integer
);
SELECT pg_catalog.setval('allocation_researchclassification_id_seq', 196, true);

--
-- Name: allocation_researchfunding_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_researchfunding_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_researchfunding; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_researchfunding (
    id serial,
    application_id integer NOT NULL,
    participant character varying(256),
    funding_source character varying(256),
    title character varying(256),
    years character varying,
    total_funding character varying
);
SELECT pg_catalog.setval('allocation_researchfunding_id_seq', 257, true);

--
-- Name: allocation_reviewercomment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_reviewercomment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_reviewercomment; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_reviewercomment (
    id serial,
    application_id integer NOT NULL,
    reviewer_comment text,
    reviewer_id integer
);
SELECT pg_catalog.setval('allocation_reviewercomment_id_seq', 231, true);

--
-- Name: allocation_reviewerscore_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_reviewerscore_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_reviewerscore; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_reviewerscore (
    id serial,
    application_id integer NOT NULL,
    research_merit integer,
    computational_merit integer,
    score integer,
    reviewer_id integer
);
SELECT pg_catalog.setval('allocation_reviewerscore_id_seq', 230, true);

--
-- Name: allocation_supercomputerjob_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_supercomputerjob_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_supercomputerjob; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_supercomputerjob (
    id serial,
    application_id integer NOT NULL,
    job_type character varying(1),
    processes integer,
    processes_per_node integer,
    wallclock_time_per_job character varying(32),
    number_of_type_of_job integer,
    total_memory character varying(32),
    data_transfer character varying(32)
);
SELECT pg_catalog.setval('allocation_supercomputerjob_id_seq', 176, true);

--
-- Name: allocation_supportingfunding_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: allocation_supportingfunding_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: allocation_supportingfunding; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE allocation_supportingfunding (
    id serial,
    application_id integer NOT NULL,
    participant character varying(256),
    funding_source character varying(256),
    title character varying(256),
    years character varying,
    total_funding character varying
);
SELECT pg_catalog.setval('allocation_supportingfunding_id_seq', 101, true);

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group (
    id serial,
    name character varying(80) NOT NULL
);
SELECT pg_catalog.setval('auth_group_id_seq', 13, true);

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id serial,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);
SELECT pg_catalog.setval('auth_group_permissions_id_seq', 148, true);

--
-- Name: auth_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: auth_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: auth_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_message (
    id serial,
    user_id integer NOT NULL,
    message text NOT NULL
);
SELECT pg_catalog.setval('auth_message_id_seq', 1773, true);

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_permission (
    id serial,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);
SELECT pg_catalog.setval('auth_permission_id_seq', 85, true);

--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user (
    id serial,
    username character varying(256) NOT NULL,
    first_name character varying(256) NOT NULL,
    last_name character varying(256) NOT NULL,
    email character varying(75) NOT NULL,
    "password" character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);
SELECT pg_catalog.setval('auth_user_id_seq', 187, true);

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id serial,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);
SELECT pg_catalog.setval('auth_user_groups_id_seq', 439, true);

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id serial,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);
SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_admin_log (
    id serial,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);
SELECT pg_catalog.setval('django_admin_log_id_seq', 1821, true);

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_content_type (
    id serial,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);
SELECT pg_catalog.setval('django_content_type_id_seq', 28, true);

--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: django_site; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_site (
    id serial,
    "domain" character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);
SELECT pg_catalog.setval('django_site_id_seq', 2, true);

--
-- Name: registration_registrationprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

-- removed in favour of serial column type


--
-- Name: registration_registrationprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: registration_registrationprofile; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE registration_registrationprofile (
    id serial,
    user_id integer NOT NULL,
    activation_key character varying(40) NOT NULL
);
SELECT pg_catalog.setval('registration_registrationprofile_id_seq', 162, true);

--
-- Name: usecaseapp_usecase_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE usecaseapp_usecase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: usecaseapp_usecase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--




--
-- Name: usecaseapp_usecase; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE usecaseapp_usecase (
    id serial,
    description character varying(1024) NOT NULL,
    submitter_id integer NOT NULL,
    created_on timestamp with time zone NOT NULL
);
SELECT pg_catalog.setval('usecaseapp_usecase_id_seq', 1, false);

--
-- Data for Name: allocation_application; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO allocation_application VALUES (103, 'First Test Application', 'This is just a test', true, false, '', '', '', NULL, '', '', '', '', 185, '2011-09-20 13:32:51.025405+08', true, false, false, false, NULL, NULL);
INSERT INTO allocation_application VALUES (104, 'Another Test Project', 'Just another test.', false, false, '', '', '', NULL, '', '', '', '', 187, '2011-09-20 13:35:11.896132+08', false, true, false, false, NULL, '');


--
-- Data for Name: allocation_fieldofresearchcode; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: allocation_institution; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO allocation_institution VALUES (1, 'CSIRO', 'CSIRO');
INSERT INTO allocation_institution VALUES (2, 'Curtin University', 'Curtin University');
INSERT INTO allocation_institution VALUES (3, 'Edith Cowan University', 'Edith Cowan University');
INSERT INTO allocation_institution VALUES (4, 'iVEC', 'iVEC');
INSERT INTO allocation_institution VALUES (5, 'Murdoch University', 'Murdoch University');
INSERT INTO allocation_institution VALUES (6, 'University of Western Australia', 'University of Western Australia');
INSERT INTO allocation_institution VALUES (7, 'External', 'National');


--
-- Data for Name: allocation_library; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: allocation_participant; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: allocation_participantaccount; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: allocation_participantstatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO allocation_participantstatus VALUES (1, 'New', 'Created as part of an application');
INSERT INTO allocation_participantstatus VALUES (2, 'Account Email Sent', 'An account creation email has been sent to the participant');
INSERT INTO allocation_participantstatus VALUES (3, 'Account Details Filled', 'The participant has filled in all the details needed to create the account');
INSERT INTO allocation_participantstatus VALUES (4, 'Account Created', 'The account has been created for the participant');
INSERT INTO allocation_participantstatus VALUES (5, 'Account Created Email Sent', 'The account creation notification email has been sent to the participant');


--
-- Data for Name: allocation_publication; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: allocation_researchclassification; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: allocation_researchfunding; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: allocation_reviewercomment; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: allocation_reviewerscore; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: allocation_supercomputerjob; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: allocation_supportingfunding; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO auth_group VALUES (3, 'reviewers_astronomy');
INSERT INTO auth_group VALUES (4, 'reviewers_directors');
INSERT INTO auth_group VALUES (5, 'reviewers_geosciences');
INSERT INTO auth_group VALUES (6, 'reviewers_national');
INSERT INTO auth_group VALUES (7, 'reviewers_partner');
INSERT INTO auth_group VALUES (12, 'privileged_reviewers');
INSERT INTO auth_group VALUES (13, 'directors');
INSERT INTO auth_group VALUES (1, 'unprivileged');


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO auth_group_permissions VALUES (6, 3, 28);
INSERT INTO auth_group_permissions VALUES (7, 3, 29);
INSERT INTO auth_group_permissions VALUES (8, 3, 30);
INSERT INTO auth_group_permissions VALUES (9, 3, 37);
INSERT INTO auth_group_permissions VALUES (10, 3, 38);
INSERT INTO auth_group_permissions VALUES (11, 3, 39);
INSERT INTO auth_group_permissions VALUES (12, 3, 43);
INSERT INTO auth_group_permissions VALUES (13, 3, 44);
INSERT INTO auth_group_permissions VALUES (14, 3, 45);
INSERT INTO auth_group_permissions VALUES (15, 3, 46);
INSERT INTO auth_group_permissions VALUES (16, 3, 47);
INSERT INTO auth_group_permissions VALUES (17, 3, 48);
INSERT INTO auth_group_permissions VALUES (18, 3, 52);
INSERT INTO auth_group_permissions VALUES (19, 3, 53);
INSERT INTO auth_group_permissions VALUES (20, 3, 54);
INSERT INTO auth_group_permissions VALUES (21, 3, 55);
INSERT INTO auth_group_permissions VALUES (22, 3, 56);
INSERT INTO auth_group_permissions VALUES (23, 3, 57);
INSERT INTO auth_group_permissions VALUES (24, 3, 58);
INSERT INTO auth_group_permissions VALUES (25, 3, 59);
INSERT INTO auth_group_permissions VALUES (26, 3, 60);
INSERT INTO auth_group_permissions VALUES (27, 3, 61);
INSERT INTO auth_group_permissions VALUES (28, 3, 62);
INSERT INTO auth_group_permissions VALUES (29, 3, 63);
INSERT INTO auth_group_permissions VALUES (30, 3, 64);
INSERT INTO auth_group_permissions VALUES (31, 3, 65);
INSERT INTO auth_group_permissions VALUES (32, 3, 66);
INSERT INTO auth_group_permissions VALUES (33, 4, 28);
INSERT INTO auth_group_permissions VALUES (34, 4, 29);
INSERT INTO auth_group_permissions VALUES (35, 4, 30);
INSERT INTO auth_group_permissions VALUES (36, 4, 37);
INSERT INTO auth_group_permissions VALUES (37, 4, 38);
INSERT INTO auth_group_permissions VALUES (38, 4, 39);
INSERT INTO auth_group_permissions VALUES (39, 4, 43);
INSERT INTO auth_group_permissions VALUES (40, 4, 44);
INSERT INTO auth_group_permissions VALUES (41, 4, 45);
INSERT INTO auth_group_permissions VALUES (42, 4, 46);
INSERT INTO auth_group_permissions VALUES (43, 4, 47);
INSERT INTO auth_group_permissions VALUES (44, 4, 48);
INSERT INTO auth_group_permissions VALUES (45, 4, 52);
INSERT INTO auth_group_permissions VALUES (46, 4, 53);
INSERT INTO auth_group_permissions VALUES (47, 4, 54);
INSERT INTO auth_group_permissions VALUES (48, 4, 55);
INSERT INTO auth_group_permissions VALUES (49, 4, 56);
INSERT INTO auth_group_permissions VALUES (50, 4, 57);
INSERT INTO auth_group_permissions VALUES (51, 4, 58);
INSERT INTO auth_group_permissions VALUES (52, 4, 59);
INSERT INTO auth_group_permissions VALUES (53, 4, 60);
INSERT INTO auth_group_permissions VALUES (54, 4, 61);
INSERT INTO auth_group_permissions VALUES (55, 4, 62);
INSERT INTO auth_group_permissions VALUES (56, 4, 63);
INSERT INTO auth_group_permissions VALUES (57, 4, 64);
INSERT INTO auth_group_permissions VALUES (58, 4, 65);
INSERT INTO auth_group_permissions VALUES (59, 4, 66);
INSERT INTO auth_group_permissions VALUES (60, 5, 28);
INSERT INTO auth_group_permissions VALUES (61, 5, 29);
INSERT INTO auth_group_permissions VALUES (62, 5, 30);
INSERT INTO auth_group_permissions VALUES (63, 5, 37);
INSERT INTO auth_group_permissions VALUES (64, 5, 38);
INSERT INTO auth_group_permissions VALUES (65, 5, 39);
INSERT INTO auth_group_permissions VALUES (66, 5, 43);
INSERT INTO auth_group_permissions VALUES (67, 5, 44);
INSERT INTO auth_group_permissions VALUES (68, 5, 45);
INSERT INTO auth_group_permissions VALUES (69, 5, 46);
INSERT INTO auth_group_permissions VALUES (70, 5, 47);
INSERT INTO auth_group_permissions VALUES (71, 5, 48);
INSERT INTO auth_group_permissions VALUES (72, 5, 52);
INSERT INTO auth_group_permissions VALUES (73, 5, 53);
INSERT INTO auth_group_permissions VALUES (74, 5, 54);
INSERT INTO auth_group_permissions VALUES (75, 5, 55);
INSERT INTO auth_group_permissions VALUES (76, 5, 56);
INSERT INTO auth_group_permissions VALUES (77, 5, 57);
INSERT INTO auth_group_permissions VALUES (78, 5, 58);
INSERT INTO auth_group_permissions VALUES (79, 5, 59);
INSERT INTO auth_group_permissions VALUES (80, 5, 60);
INSERT INTO auth_group_permissions VALUES (81, 5, 61);
INSERT INTO auth_group_permissions VALUES (82, 5, 62);
INSERT INTO auth_group_permissions VALUES (83, 5, 63);
INSERT INTO auth_group_permissions VALUES (84, 5, 64);
INSERT INTO auth_group_permissions VALUES (85, 5, 65);
INSERT INTO auth_group_permissions VALUES (86, 5, 66);
INSERT INTO auth_group_permissions VALUES (87, 6, 28);
INSERT INTO auth_group_permissions VALUES (88, 6, 29);
INSERT INTO auth_group_permissions VALUES (89, 6, 30);
INSERT INTO auth_group_permissions VALUES (90, 6, 37);
INSERT INTO auth_group_permissions VALUES (91, 6, 38);
INSERT INTO auth_group_permissions VALUES (92, 6, 39);
INSERT INTO auth_group_permissions VALUES (93, 6, 43);
INSERT INTO auth_group_permissions VALUES (94, 6, 44);
INSERT INTO auth_group_permissions VALUES (95, 6, 45);
INSERT INTO auth_group_permissions VALUES (96, 6, 46);
INSERT INTO auth_group_permissions VALUES (97, 6, 47);
INSERT INTO auth_group_permissions VALUES (98, 6, 48);
INSERT INTO auth_group_permissions VALUES (99, 6, 52);
INSERT INTO auth_group_permissions VALUES (100, 6, 53);
INSERT INTO auth_group_permissions VALUES (101, 6, 54);
INSERT INTO auth_group_permissions VALUES (102, 6, 55);
INSERT INTO auth_group_permissions VALUES (103, 6, 56);
INSERT INTO auth_group_permissions VALUES (104, 6, 57);
INSERT INTO auth_group_permissions VALUES (105, 6, 58);
INSERT INTO auth_group_permissions VALUES (106, 6, 59);
INSERT INTO auth_group_permissions VALUES (107, 6, 60);
INSERT INTO auth_group_permissions VALUES (108, 6, 61);
INSERT INTO auth_group_permissions VALUES (109, 6, 62);
INSERT INTO auth_group_permissions VALUES (110, 6, 63);
INSERT INTO auth_group_permissions VALUES (111, 6, 64);
INSERT INTO auth_group_permissions VALUES (112, 6, 65);
INSERT INTO auth_group_permissions VALUES (113, 6, 66);
INSERT INTO auth_group_permissions VALUES (114, 7, 28);
INSERT INTO auth_group_permissions VALUES (115, 7, 29);
INSERT INTO auth_group_permissions VALUES (116, 7, 30);
INSERT INTO auth_group_permissions VALUES (117, 7, 37);
INSERT INTO auth_group_permissions VALUES (118, 7, 38);
INSERT INTO auth_group_permissions VALUES (119, 7, 39);
INSERT INTO auth_group_permissions VALUES (120, 7, 43);
INSERT INTO auth_group_permissions VALUES (121, 7, 44);
INSERT INTO auth_group_permissions VALUES (122, 7, 45);
INSERT INTO auth_group_permissions VALUES (123, 7, 46);
INSERT INTO auth_group_permissions VALUES (124, 7, 47);
INSERT INTO auth_group_permissions VALUES (125, 7, 48);
INSERT INTO auth_group_permissions VALUES (126, 7, 52);
INSERT INTO auth_group_permissions VALUES (127, 7, 53);
INSERT INTO auth_group_permissions VALUES (128, 7, 54);
INSERT INTO auth_group_permissions VALUES (129, 7, 55);
INSERT INTO auth_group_permissions VALUES (130, 7, 56);
INSERT INTO auth_group_permissions VALUES (131, 7, 57);
INSERT INTO auth_group_permissions VALUES (132, 7, 58);
INSERT INTO auth_group_permissions VALUES (133, 7, 59);
INSERT INTO auth_group_permissions VALUES (134, 7, 60);
INSERT INTO auth_group_permissions VALUES (135, 7, 61);
INSERT INTO auth_group_permissions VALUES (136, 7, 62);
INSERT INTO auth_group_permissions VALUES (137, 7, 63);
INSERT INTO auth_group_permissions VALUES (138, 7, 64);
INSERT INTO auth_group_permissions VALUES (139, 7, 65);
INSERT INTO auth_group_permissions VALUES (140, 7, 66);
INSERT INTO auth_group_permissions VALUES (142, 12, 70);
INSERT INTO auth_group_permissions VALUES (143, 12, 71);
INSERT INTO auth_group_permissions VALUES (144, 12, 73);
INSERT INTO auth_group_permissions VALUES (145, 12, 74);
INSERT INTO auth_group_permissions VALUES (146, 1, 28);
INSERT INTO auth_group_permissions VALUES (147, 1, 29);
INSERT INTO auth_group_permissions VALUES (148, 1, 30);


--
-- Data for Name: auth_message; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO auth_permission VALUES (1, 'Can add permission', 1, 'add_permission');
INSERT INTO auth_permission VALUES (2, 'Can change permission', 1, 'change_permission');
INSERT INTO auth_permission VALUES (3, 'Can delete permission', 1, 'delete_permission');
INSERT INTO auth_permission VALUES (4, 'Can add group', 2, 'add_group');
INSERT INTO auth_permission VALUES (5, 'Can change group', 2, 'change_group');
INSERT INTO auth_permission VALUES (6, 'Can delete group', 2, 'delete_group');
INSERT INTO auth_permission VALUES (7, 'Can add user', 3, 'add_user');
INSERT INTO auth_permission VALUES (8, 'Can change user', 3, 'change_user');
INSERT INTO auth_permission VALUES (9, 'Can delete user', 3, 'delete_user');
INSERT INTO auth_permission VALUES (10, 'Can add message', 4, 'add_message');
INSERT INTO auth_permission VALUES (11, 'Can change message', 4, 'change_message');
INSERT INTO auth_permission VALUES (12, 'Can delete message', 4, 'delete_message');
INSERT INTO auth_permission VALUES (13, 'Can add content type', 5, 'add_contenttype');
INSERT INTO auth_permission VALUES (14, 'Can change content type', 5, 'change_contenttype');
INSERT INTO auth_permission VALUES (15, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO auth_permission VALUES (16, 'Can add session', 6, 'add_session');
INSERT INTO auth_permission VALUES (17, 'Can change session', 6, 'change_session');
INSERT INTO auth_permission VALUES (18, 'Can delete session', 6, 'delete_session');
INSERT INTO auth_permission VALUES (19, 'Can add site', 7, 'add_site');
INSERT INTO auth_permission VALUES (20, 'Can change site', 7, 'change_site');
INSERT INTO auth_permission VALUES (21, 'Can delete site', 7, 'delete_site');
INSERT INTO auth_permission VALUES (22, 'Can add registration profile', 8, 'add_registrationprofile');
INSERT INTO auth_permission VALUES (23, 'Can change registration profile', 8, 'change_registrationprofile');
INSERT INTO auth_permission VALUES (24, 'Can delete registration profile', 8, 'delete_registrationprofile');
INSERT INTO auth_permission VALUES (25, 'Can add log entry', 9, 'add_logentry');
INSERT INTO auth_permission VALUES (26, 'Can change log entry', 9, 'change_logentry');
INSERT INTO auth_permission VALUES (27, 'Can delete log entry', 9, 'delete_logentry');
INSERT INTO auth_permission VALUES (28, 'Can add application', 10, 'add_application');
INSERT INTO auth_permission VALUES (29, 'Can change application', 10, 'change_application');
INSERT INTO auth_permission VALUES (30, 'Can delete application', 10, 'delete_application');
INSERT INTO auth_permission VALUES (37, 'Can add participant', 13, 'add_participant');
INSERT INTO auth_permission VALUES (38, 'Can change participant', 13, 'change_participant');
INSERT INTO auth_permission VALUES (39, 'Can delete participant', 13, 'delete_participant');
INSERT INTO auth_permission VALUES (43, 'Can add research funding', 15, 'add_researchfunding');
INSERT INTO auth_permission VALUES (44, 'Can change research funding', 15, 'change_researchfunding');
INSERT INTO auth_permission VALUES (45, 'Can delete research funding', 15, 'delete_researchfunding');
INSERT INTO auth_permission VALUES (46, 'Can add supercomputer job', 16, 'add_supercomputerjob');
INSERT INTO auth_permission VALUES (47, 'Can change supercomputer job', 16, 'change_supercomputerjob');
INSERT INTO auth_permission VALUES (48, 'Can delete supercomputer job', 16, 'delete_supercomputerjob');
INSERT INTO auth_permission VALUES (52, 'Can add research classification', 18, 'add_researchclassification');
INSERT INTO auth_permission VALUES (53, 'Can change research classification', 18, 'change_researchclassification');
INSERT INTO auth_permission VALUES (54, 'Can delete research classification', 18, 'delete_researchclassification');
INSERT INTO auth_permission VALUES (55, 'Can add field of research code', 19, 'add_fieldofresearchcode');
INSERT INTO auth_permission VALUES (56, 'Can change field of research code', 19, 'change_fieldofresearchcode');
INSERT INTO auth_permission VALUES (57, 'Can delete field of research code', 19, 'delete_fieldofresearchcode');
INSERT INTO auth_permission VALUES (58, 'Can add publication', 20, 'add_publication');
INSERT INTO auth_permission VALUES (59, 'Can change publication', 20, 'change_publication');
INSERT INTO auth_permission VALUES (60, 'Can delete publication', 20, 'delete_publication');
INSERT INTO auth_permission VALUES (61, 'Can add library', 21, 'add_library');
INSERT INTO auth_permission VALUES (62, 'Can change library', 21, 'change_library');
INSERT INTO auth_permission VALUES (63, 'Can delete library', 21, 'delete_library');
INSERT INTO auth_permission VALUES (64, 'Can add supporting funding', 22, 'add_supportingfunding');
INSERT INTO auth_permission VALUES (65, 'Can change supporting funding', 22, 'change_supportingfunding');
INSERT INTO auth_permission VALUES (66, 'Can delete supporting funding', 22, 'delete_supportingfunding');
INSERT INTO auth_permission VALUES (67, 'Can add usecase', 26, 'add_usecase');
INSERT INTO auth_permission VALUES (68, 'Can change usecase', 26, 'change_usecase');
INSERT INTO auth_permission VALUES (69, 'Can delete usecase', 26, 'delete_usecase');
INSERT INTO auth_permission VALUES (70, 'Can add reviewer score', 23, 'add_reviewerscore');
INSERT INTO auth_permission VALUES (71, 'Can change reviewer score', 23, 'change_reviewerscore');
INSERT INTO auth_permission VALUES (72, 'Can delete reviewer score', 23, 'delete_reviewerscore');
INSERT INTO auth_permission VALUES (73, 'Can add reviewer comment', 24, 'add_reviewercomment');
INSERT INTO auth_permission VALUES (74, 'Can change reviewer comment', 24, 'change_reviewercomment');
INSERT INTO auth_permission VALUES (75, 'Can delete reviewer comment', 24, 'delete_reviewercomment');
INSERT INTO auth_permission VALUES (76, 'Can add participant status', 27, 'add_participantstatus');
INSERT INTO auth_permission VALUES (77, 'Can change participant status', 27, 'change_participantstatus');
INSERT INTO auth_permission VALUES (78, 'Can delete participant status', 27, 'delete_participantstatus');
INSERT INTO auth_permission VALUES (79, 'Can add institution', 28, 'add_institution');
INSERT INTO auth_permission VALUES (80, 'Can change institution', 28, 'change_institution');
INSERT INTO auth_permission VALUES (81, 'Can delete institution', 28, 'delete_institution');
INSERT INTO auth_permission VALUES (82, 'Can add participant account', 25, 'add_participantaccount');
INSERT INTO auth_permission VALUES (83, 'Can change participant account', 25, 'change_participantaccount');
INSERT INTO auth_permission VALUES (84, 'Can delete participant account', 25, 'delete_participantaccount');


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO auth_user VALUES (186, 'reviewer', '', '', '', 'sha1$56536$04f1b4c946d6f76ef3e1523dc3449c44685a4af9', true, true, false, '2011-09-20 13:24:24+08', '2011-09-20 13:24:24+08');
INSERT INTO auth_user VALUES (185, 'user', '', '', '', 'sha1$2cd15$dd82c8f8744365ba382d029962811e48200b60be', true, true, false, '2011-09-20 13:25:29.000276+08', '2011-09-20 13:23:34+08');
INSERT INTO auth_user VALUES (187, 'director', '', '', '', 'sha1$34cde$15b88427bb024a185c434a92af78a5b57474880a', true, true, false, '2011-09-20 13:34:40.203217+08', '2011-09-20 13:24:50+08');
INSERT INTO auth_user VALUES (1, 'admin', 'Allocation', 'Admin', 'bpower@ccg.murdoch.edu.au', 'sha1$e30f7$29a46dbbc433a0a8a165541782fbde675e8cfa75', true, true, true, '2011-09-20 13:35:23.999622+08', '2011-08-24 11:01:52+08');


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO auth_user_groups VALUES (402, 1, 1);
INSERT INTO auth_user_groups VALUES (403, 1, 12);
INSERT INTO auth_user_groups VALUES (419, 185, 1);
INSERT INTO auth_user_groups VALUES (420, 185, 3);
INSERT INTO auth_user_groups VALUES (421, 185, 4);
INSERT INTO auth_user_groups VALUES (422, 185, 5);
INSERT INTO auth_user_groups VALUES (423, 185, 6);
INSERT INTO auth_user_groups VALUES (424, 185, 7);
INSERT INTO auth_user_groups VALUES (425, 186, 1);
INSERT INTO auth_user_groups VALUES (426, 186, 3);
INSERT INTO auth_user_groups VALUES (427, 186, 4);
INSERT INTO auth_user_groups VALUES (428, 186, 5);
INSERT INTO auth_user_groups VALUES (429, 186, 6);
INSERT INTO auth_user_groups VALUES (430, 186, 7);
INSERT INTO auth_user_groups VALUES (431, 186, 12);
INSERT INTO auth_user_groups VALUES (432, 187, 1);
INSERT INTO auth_user_groups VALUES (433, 187, 3);
INSERT INTO auth_user_groups VALUES (434, 187, 4);
INSERT INTO auth_user_groups VALUES (435, 187, 5);
INSERT INTO auth_user_groups VALUES (436, 187, 6);
INSERT INTO auth_user_groups VALUES (437, 187, 7);
INSERT INTO auth_user_groups VALUES (438, 187, 12);
INSERT INTO auth_user_groups VALUES (439, 187, 13);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO django_content_type VALUES (1, 'permission', 'auth', 'permission');
INSERT INTO django_content_type VALUES (2, 'group', 'auth', 'group');
INSERT INTO django_content_type VALUES (3, 'user', 'auth', 'user');
INSERT INTO django_content_type VALUES (4, 'message', 'auth', 'message');
INSERT INTO django_content_type VALUES (5, 'content type', 'contenttypes', 'contenttype');
INSERT INTO django_content_type VALUES (6, 'session', 'sessions', 'session');
INSERT INTO django_content_type VALUES (7, 'site', 'sites', 'site');
INSERT INTO django_content_type VALUES (8, 'registration profile', 'registration', 'registrationprofile');
INSERT INTO django_content_type VALUES (9, 'log entry', 'admin', 'logentry');
INSERT INTO django_content_type VALUES (10, 'application', 'allocation', 'application');
INSERT INTO django_content_type VALUES (13, 'participant', 'allocation', 'participant');
INSERT INTO django_content_type VALUES (15, 'research funding', 'allocation', 'researchfunding');
INSERT INTO django_content_type VALUES (16, 'supercomputer job', 'allocation', 'supercomputerjob');
INSERT INTO django_content_type VALUES (18, 'research classification', 'allocation', 'researchclassification');
INSERT INTO django_content_type VALUES (19, 'field of research code', 'allocation', 'fieldofresearchcode');
INSERT INTO django_content_type VALUES (20, 'publication', 'allocation', 'publication');
INSERT INTO django_content_type VALUES (21, 'library', 'allocation', 'library');
INSERT INTO django_content_type VALUES (22, 'supporting funding', 'allocation', 'supportingfunding');
INSERT INTO django_content_type VALUES (23, 'reviewer score', 'allocation', 'reviewerscore');
INSERT INTO django_content_type VALUES (24, 'reviewer comment', 'allocation', 'reviewercomment');
INSERT INTO django_content_type VALUES (25, 'participant account', 'allocation', 'participantaccount');
INSERT INTO django_content_type VALUES (26, 'usecase', 'usecaseapp', 'usecase');
INSERT INTO django_content_type VALUES (27, 'participant status', 'allocation', 'participantstatus');
INSERT INTO django_content_type VALUES (28, 'institution', 'allocation', 'institution');


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO django_site VALUES (1, '127.0.0.1', 'localdev-usecase');
INSERT INTO django_site VALUES (2, 'ccg.murdoch.edu.au/usecase', 'live-usecase');


--
-- Data for Name: registration_registrationprofile; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Data for Name: usecaseapp_usecase; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- Name: allocation_application_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_application
    ADD CONSTRAINT allocation_application_pkey PRIMARY KEY (id);


--
-- Name: allocation_fieldofresearchcode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_fieldofresearchcode
    ADD CONSTRAINT allocation_fieldofresearchcode_pkey PRIMARY KEY (id);


--
-- Name: allocation_institution_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_institution
    ADD CONSTRAINT allocation_institution_pkey PRIMARY KEY (id);


--
-- Name: allocation_library_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_library
    ADD CONSTRAINT allocation_library_pkey PRIMARY KEY (id);


--
-- Name: allocation_participant_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_participant
    ADD CONSTRAINT allocation_participant_pkey PRIMARY KEY (id);


--
-- Name: allocation_participantaccount_participant_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_participantaccount
    ADD CONSTRAINT allocation_participantaccount_participant_id_key UNIQUE (participant_id);


--
-- Name: allocation_participantaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_participantaccount
    ADD CONSTRAINT allocation_participantaccount_pkey PRIMARY KEY (id);


--
-- Name: allocation_participantstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_participantstatus
    ADD CONSTRAINT allocation_participantstatus_pkey PRIMARY KEY (id);


--
-- Name: allocation_publication_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_publication
    ADD CONSTRAINT allocation_publication_pkey PRIMARY KEY (id);


--
-- Name: allocation_researchclassification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_researchclassification
    ADD CONSTRAINT allocation_researchclassification_pkey PRIMARY KEY (id);


--
-- Name: allocation_researchfunding_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_researchfunding
    ADD CONSTRAINT allocation_researchfunding_pkey PRIMARY KEY (id);


--
-- Name: allocation_reviewercomment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_reviewercomment
    ADD CONSTRAINT allocation_reviewercomment_pkey PRIMARY KEY (id);


--
-- Name: allocation_reviewerscore_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_reviewerscore
    ADD CONSTRAINT allocation_reviewerscore_pkey PRIMARY KEY (id);


--
-- Name: allocation_supercomputerjob_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_supercomputerjob
    ADD CONSTRAINT allocation_supercomputerjob_pkey PRIMARY KEY (id);


--
-- Name: allocation_supportingfunding_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY allocation_supportingfunding
    ADD CONSTRAINT allocation_supportingfunding_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: registration_registrationprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY registration_registrationprofile
    ADD CONSTRAINT registration_registrationprofile_pkey PRIMARY KEY (id);


--
-- Name: registration_registrationprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY registration_registrationprofile
    ADD CONSTRAINT registration_registrationprofile_user_id_key UNIQUE (user_id);


--
-- Name: usecaseapp_usecase_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY usecaseapp_usecase
    ADD CONSTRAINT usecaseapp_usecase_pkey PRIMARY KEY (id);


--
-- Name: allocation_application_created_by_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_application_created_by_id ON allocation_application USING btree (created_by_id);


--
-- Name: allocation_library_application_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_library_application_id ON allocation_library USING btree (application_id);


--
-- Name: allocation_participant_application_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_participant_application_id ON allocation_participant USING btree (application_id);


--
-- Name: allocation_participant_status_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_participant_status_id ON allocation_participant USING btree (status_id);


--
-- Name: allocation_publication_application_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_publication_application_id ON allocation_publication USING btree (application_id);


--
-- Name: allocation_researchclassification_application_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_researchclassification_application_id ON allocation_researchclassification USING btree (application_id);


--
-- Name: allocation_researchfunding_application_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_researchfunding_application_id ON allocation_researchfunding USING btree (application_id);


--
-- Name: allocation_reviewercomment_application_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_reviewercomment_application_id ON allocation_reviewercomment USING btree (application_id);


--
-- Name: allocation_reviewercomment_reviewer_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_reviewercomment_reviewer_id ON allocation_reviewercomment USING btree (reviewer_id);


--
-- Name: allocation_reviewerscore_application_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_reviewerscore_application_id ON allocation_reviewerscore USING btree (application_id);


--
-- Name: allocation_reviewerscore_reviewer_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_reviewerscore_reviewer_id ON allocation_reviewerscore USING btree (reviewer_id);


--
-- Name: allocation_supercomputerjob_application_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_supercomputerjob_application_id ON allocation_supercomputerjob USING btree (application_id);


--
-- Name: allocation_supportingfunding_application_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX allocation_supportingfunding_application_id ON allocation_supportingfunding USING btree (application_id);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_message_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_message_user_id ON auth_message USING btree (user_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: usecaseapp_usecase_submitter_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX usecaseapp_usecase_submitter_id ON usecaseapp_usecase USING btree (submitter_id);


--
-- Name: allocation_application_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_application
    ADD CONSTRAINT allocation_application_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_library_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_library
    ADD CONSTRAINT allocation_library_application_id_fkey FOREIGN KEY (application_id) REFERENCES allocation_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_participant_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_participant
    ADD CONSTRAINT allocation_participant_application_id_fkey FOREIGN KEY (application_id) REFERENCES allocation_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_participant_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_participant
    ADD CONSTRAINT allocation_participant_status_id_fkey FOREIGN KEY (status_id) REFERENCES allocation_participantstatus(id);


--
-- Name: allocation_participantaccount_institution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_participantaccount
    ADD CONSTRAINT allocation_participantaccount_institution_id_fkey FOREIGN KEY (institution_id) REFERENCES allocation_institution(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_participantaccount_participant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_participantaccount
    ADD CONSTRAINT allocation_participantaccount_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES allocation_participant(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_publication_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_publication
    ADD CONSTRAINT allocation_publication_application_id_fkey FOREIGN KEY (application_id) REFERENCES allocation_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_researchclassification_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_researchclassification
    ADD CONSTRAINT allocation_researchclassification_application_id_fkey FOREIGN KEY (application_id) REFERENCES allocation_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_researchfunding_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_researchfunding
    ADD CONSTRAINT allocation_researchfunding_application_id_fkey FOREIGN KEY (application_id) REFERENCES allocation_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_reviewercomment_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_reviewercomment
    ADD CONSTRAINT allocation_reviewercomment_application_id_fkey FOREIGN KEY (application_id) REFERENCES allocation_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_reviewercomment_reviewer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_reviewercomment
    ADD CONSTRAINT allocation_reviewercomment_reviewer_id_fkey FOREIGN KEY (reviewer_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_reviewerscore_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_reviewerscore
    ADD CONSTRAINT allocation_reviewerscore_application_id_fkey FOREIGN KEY (application_id) REFERENCES allocation_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_reviewerscore_reviewer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_reviewerscore
    ADD CONSTRAINT allocation_reviewerscore_reviewer_id_fkey FOREIGN KEY (reviewer_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_supercomputerjob_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_supercomputerjob
    ADD CONSTRAINT allocation_supercomputerjob_application_id_fkey FOREIGN KEY (application_id) REFERENCES allocation_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: allocation_supportingfunding_application_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY allocation_supportingfunding
    ADD CONSTRAINT allocation_supportingfunding_application_id_fkey FOREIGN KEY (application_id) REFERENCES allocation_application(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_728de91f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_3cea63fe; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT group_id_refs_id_3cea63fe FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: registration_registrationprofile_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY registration_registrationprofile
    ADD CONSTRAINT registration_registrationprofile_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: usecaseapp_usecase_submitter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY usecaseapp_usecase
    ADD CONSTRAINT usecaseapp_usecase_submitter_id_fkey FOREIGN KEY (submitter_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_831107f1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT user_id_refs_id_831107f1 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_f2045483; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT user_id_refs_id_f2045483 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

