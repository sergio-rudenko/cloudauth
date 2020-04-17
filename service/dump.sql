--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE IF EXISTS cloudauth_db;
--
-- Name: cloudauth_db; Type: DATABASE; Schema: -; Owner: cloudauth
--

CREATE DATABASE cloudauth_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.utf8' LC_CTYPE = 'en_US.utf8';


ALTER DATABASE cloudauth_db OWNER TO cloudauth;

\connect cloudauth_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: hashes; Type: TABLE; Schema: public; Owner: cloudauth
--

CREATE TABLE public.hashes (
    user_id integer NOT NULL,
    key character varying(64) NOT NULL,
    description character varying,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL
);


ALTER TABLE public.hashes OWNER TO cloudauth;

--
-- Name: tokens; Type: TABLE; Schema: public; Owner: cloudauth
--

CREATE TABLE public.tokens (
    user_id integer NOT NULL,
    key character varying(32) NOT NULL,
    description character varying,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL
);


ALTER TABLE public.tokens OWNER TO cloudauth;

--
-- Name: users; Type: TABLE; Schema: public; Owner: cloudauth
--

CREATE TABLE public.users (
    id integer NOT NULL,
    phone character varying(16) NOT NULL,
    description character varying,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL
);


ALTER TABLE public.users OWNER TO cloudauth;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: cloudauth
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO cloudauth;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: cloudauth
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: cloudauth
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: hashes; Type: TABLE DATA; Schema: public; Owner: cloudauth
--

COPY public.hashes (user_id, key, description, created, updated) FROM stdin;
1	1234567890	test	2020-04-17 20:51:31.014736	2020-04-17 20:51:31.014736
\.


--
-- Data for Name: tokens; Type: TABLE DATA; Schema: public; Owner: cloudauth
--

COPY public.tokens (user_id, key, description, created, updated) FROM stdin;
1	qwertyuiop	test	2020-04-17 20:52:33.83637	2020-04-17 20:52:33.83637
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: cloudauth
--

COPY public.users (id, phone, description, created, updated) FROM stdin;
1	+79185387721	created by create_user_hash	2020-04-17 20:51:31.00013	2020-04-17 20:51:31.00013
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: cloudauth
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: hashes hashes_pkey; Type: CONSTRAINT; Schema: public; Owner: cloudauth
--

ALTER TABLE ONLY public.hashes
    ADD CONSTRAINT hashes_pkey PRIMARY KEY (key);


--
-- Name: tokens tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: cloudauth
--

ALTER TABLE ONLY public.tokens
    ADD CONSTRAINT tokens_pkey PRIMARY KEY (key);


--
-- Name: users users_phone_key; Type: CONSTRAINT; Schema: public; Owner: cloudauth
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_phone_key UNIQUE (phone);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: cloudauth
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: hashes hashes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cloudauth
--

ALTER TABLE ONLY public.hashes
    ADD CONSTRAINT hashes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: tokens tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cloudauth
--

ALTER TABLE ONLY public.tokens
    ADD CONSTRAINT tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

