--
-- PostgreSQL database dump
--

-- Dumped from database version 12.17 (Ubuntu 12.17-1.pgdg22.04+1)
-- Dumped by pg_dump version 12.17 (Ubuntu 12.17-1.pgdg22.04+1)

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

DROP DATABASE universe;
--
-- Name: universe; Type: DATABASE; Schema: -; Owner: freecodecamp
--

CREATE DATABASE universe WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'C.UTF-8' LC_CTYPE = 'C.UTF-8';


ALTER DATABASE universe OWNER TO freecodecamp;

\connect universe

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
-- Name: asteroids; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.asteroids (
    asteroids_id integer NOT NULL,
    name character varying(30),
    int1 integer NOT NULL,
    int2 integer,
    "numeric" numeric(4,1),
    text text,
    boolen boolean
);


ALTER TABLE public.asteroids OWNER TO freecodecamp;

--
-- Name: asteroids_asteroids_id_seq; Type: SEQUENCE; Schema: public; Owner: freecodecamp
--

CREATE SEQUENCE public.asteroids_asteroids_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.asteroids_asteroids_id_seq OWNER TO freecodecamp;

--
-- Name: asteroids_asteroids_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: freecodecamp
--

ALTER SEQUENCE public.asteroids_asteroids_id_seq OWNED BY public.asteroids.asteroids_id;


--
-- Name: galaxy; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.galaxy (
    galaxy_id integer NOT NULL,
    name character varying(30),
    int1 integer,
    int2 integer,
    "numeric" numeric(4,1) NOT NULL,
    text text,
    "boolean" boolean
);


ALTER TABLE public.galaxy OWNER TO freecodecamp;

--
-- Name: galaxy_galaxy_id_seq; Type: SEQUENCE; Schema: public; Owner: freecodecamp
--

CREATE SEQUENCE public.galaxy_galaxy_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.galaxy_galaxy_id_seq OWNER TO freecodecamp;

--
-- Name: galaxy_galaxy_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: freecodecamp
--

ALTER SEQUENCE public.galaxy_galaxy_id_seq OWNED BY public.galaxy.galaxy_id;


--
-- Name: moon; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.moon (
    moon_id integer NOT NULL,
    name character varying(30),
    int1 integer NOT NULL,
    int2 integer,
    "numeric" numeric(4,1),
    text text,
    "boolean" boolean,
    planet_id integer
);


ALTER TABLE public.moon OWNER TO freecodecamp;

--
-- Name: moon_moon_id_seq; Type: SEQUENCE; Schema: public; Owner: freecodecamp
--

CREATE SEQUENCE public.moon_moon_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.moon_moon_id_seq OWNER TO freecodecamp;

--
-- Name: moon_moon_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: freecodecamp
--

ALTER SEQUENCE public.moon_moon_id_seq OWNED BY public.moon.moon_id;


--
-- Name: planet; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.planet (
    planet_id integer NOT NULL,
    name character varying(30),
    int1 integer NOT NULL,
    int2 integer,
    "numeric" numeric(4,1),
    text text,
    "boolean" boolean,
    star_id integer
);


ALTER TABLE public.planet OWNER TO freecodecamp;

--
-- Name: planet_planet_id_seq; Type: SEQUENCE; Schema: public; Owner: freecodecamp
--

CREATE SEQUENCE public.planet_planet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.planet_planet_id_seq OWNER TO freecodecamp;

--
-- Name: planet_planet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: freecodecamp
--

ALTER SEQUENCE public.planet_planet_id_seq OWNED BY public.planet.planet_id;


--
-- Name: star; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.star (
    star_id integer NOT NULL,
    name character varying(30),
    int1 integer,
    int2 integer,
    "numeric" numeric(4,1),
    text text,
    "boolean" boolean,
    galaxy_id integer NOT NULL
);


ALTER TABLE public.star OWNER TO freecodecamp;

--
-- Name: star_star_id_seq; Type: SEQUENCE; Schema: public; Owner: freecodecamp
--

CREATE SEQUENCE public.star_star_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.star_star_id_seq OWNER TO freecodecamp;

--
-- Name: star_star_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: freecodecamp
--

ALTER SEQUENCE public.star_star_id_seq OWNED BY public.star.star_id;


--
-- Name: asteroids asteroids_id; Type: DEFAULT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.asteroids ALTER COLUMN asteroids_id SET DEFAULT nextval('public.asteroids_asteroids_id_seq'::regclass);


--
-- Name: galaxy galaxy_id; Type: DEFAULT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.galaxy ALTER COLUMN galaxy_id SET DEFAULT nextval('public.galaxy_galaxy_id_seq'::regclass);


--
-- Name: moon moon_id; Type: DEFAULT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.moon ALTER COLUMN moon_id SET DEFAULT nextval('public.moon_moon_id_seq'::regclass);


--
-- Name: planet planet_id; Type: DEFAULT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.planet ALTER COLUMN planet_id SET DEFAULT nextval('public.planet_planet_id_seq'::regclass);


--
-- Name: star star_id; Type: DEFAULT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star ALTER COLUMN star_id SET DEFAULT nextval('public.star_star_id_seq'::regclass);


--
-- Data for Name: asteroids; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.asteroids VALUES (1, 'asteroids1', 23, 34, 3.2, 'some text', true);
INSERT INTO public.asteroids VALUES (2, 'asteroids2', 23, 34, 3.2, 'some text', true);
INSERT INTO public.asteroids VALUES (3, 'asteroids3', 23, 34, 3.2, 'some text', true);


--
-- Data for Name: galaxy; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.galaxy VALUES (1, 'galaxy1', 23, 34, 3.2, 'some text', true);
INSERT INTO public.galaxy VALUES (2, 'galaxy2', 23, 34, 3.2, 'some text', true);
INSERT INTO public.galaxy VALUES (3, 'galaxy3', 23, 34, 3.2, 'some text', true);
INSERT INTO public.galaxy VALUES (4, 'galaxy4', 23, 34, 3.2, 'some text', true);
INSERT INTO public.galaxy VALUES (5, 'galaxy5', 23, 34, 3.2, 'some text', true);
INSERT INTO public.galaxy VALUES (6, 'galaxy6', 23, 34, 3.2, 'some text', true);


--
-- Data for Name: moon; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.moon VALUES (1, 'moon1', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.moon VALUES (2, 'moon2', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.moon VALUES (3, 'moon3', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.moon VALUES (4, 'moon4', 23, 34, 3.2, 'some text', true, 5);
INSERT INTO public.moon VALUES (5, 'moon5', 23, 34, 3.2, 'some text', true, 5);
INSERT INTO public.moon VALUES (6, 'moon6', 23, 34, 3.2, 'some text', true, 5);
INSERT INTO public.moon VALUES (7, 'moon7', 23, 34, 3.2, 'some text', true, 5);
INSERT INTO public.moon VALUES (8, 'moon8', 23, 34, 3.2, 'some text', true, 5);
INSERT INTO public.moon VALUES (9, 'moon9', 23, 34, 3.2, 'some text', true, 8);
INSERT INTO public.moon VALUES (10, 'moon10', 23, 34, 3.2, 'some text', true, 8);
INSERT INTO public.moon VALUES (11, 'moon11', 23, 34, 3.2, 'some text', true, 8);
INSERT INTO public.moon VALUES (12, 'moon12', 23, 34, 3.2, 'some text', true, 8);
INSERT INTO public.moon VALUES (13, 'moon13', 23, 34, 3.2, 'some text', true, 8);
INSERT INTO public.moon VALUES (14, 'moon14', 23, 34, 3.2, 'some text', true, 8);
INSERT INTO public.moon VALUES (15, 'moon15', 23, 34, 3.2, 'some text', true, 8);
INSERT INTO public.moon VALUES (16, 'moon16', 23, 34, 3.2, 'some text', true, 12);
INSERT INTO public.moon VALUES (17, 'moon17', 23, 34, 3.2, 'some text', true, 12);
INSERT INTO public.moon VALUES (18, 'moon18', 23, 34, 3.2, 'some text', true, 12);
INSERT INTO public.moon VALUES (19, 'moon19', 23, 34, 3.2, 'some text', true, 12);
INSERT INTO public.moon VALUES (20, 'moon20', 23, 34, 3.2, 'some text', true, 12);


--
-- Data for Name: planet; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.planet VALUES (2, 'planet2', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.planet VALUES (1, 'planet1', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.planet VALUES (3, 'planet3', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.planet VALUES (4, 'planet4', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.planet VALUES (5, 'planet5', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.planet VALUES (6, 'planet6', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.planet VALUES (7, 'planet7', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.planet VALUES (8, 'planet8', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.planet VALUES (9, 'planet9', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.planet VALUES (10, 'planet10', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.planet VALUES (11, 'planet11', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.planet VALUES (12, 'planet12', 23, 34, 3.2, 'some text', true, 1);


--
-- Data for Name: star; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.star VALUES (1, 'star1', 23, 34, 3.2, 'some text', true, 1);
INSERT INTO public.star VALUES (2, 'star2', 23, 34, 3.2, 'some text', true, 2);
INSERT INTO public.star VALUES (3, 'star3', 23, 34, 3.2, 'some text', true, 3);
INSERT INTO public.star VALUES (4, 'star4', 23, 34, 3.2, 'some text', true, 4);
INSERT INTO public.star VALUES (5, 'star5', 23, 34, 3.2, 'some text', true, 5);
INSERT INTO public.star VALUES (6, 'star6', 23, 34, 3.2, 'some text', true, 6);


--
-- Name: asteroids_asteroids_id_seq; Type: SEQUENCE SET; Schema: public; Owner: freecodecamp
--

SELECT pg_catalog.setval('public.asteroids_asteroids_id_seq', 3, true);


--
-- Name: galaxy_galaxy_id_seq; Type: SEQUENCE SET; Schema: public; Owner: freecodecamp
--

SELECT pg_catalog.setval('public.galaxy_galaxy_id_seq', 6, true);


--
-- Name: moon_moon_id_seq; Type: SEQUENCE SET; Schema: public; Owner: freecodecamp
--

SELECT pg_catalog.setval('public.moon_moon_id_seq', 20, true);


--
-- Name: planet_planet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: freecodecamp
--

SELECT pg_catalog.setval('public.planet_planet_id_seq', 12, true);


--
-- Name: star_star_id_seq; Type: SEQUENCE SET; Schema: public; Owner: freecodecamp
--

SELECT pg_catalog.setval('public.star_star_id_seq', 6, true);


--
-- Name: asteroids asteroids_asteroids_id_key; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.asteroids
    ADD CONSTRAINT asteroids_asteroids_id_key UNIQUE (asteroids_id);


--
-- Name: asteroids asteroids_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.asteroids
    ADD CONSTRAINT asteroids_pkey PRIMARY KEY (asteroids_id);


--
-- Name: galaxy galaxy_galaxy_id_key; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.galaxy
    ADD CONSTRAINT galaxy_galaxy_id_key UNIQUE (galaxy_id);


--
-- Name: galaxy galaxy_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.galaxy
    ADD CONSTRAINT galaxy_pkey PRIMARY KEY (galaxy_id);


--
-- Name: moon moon_moon_id_key; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.moon
    ADD CONSTRAINT moon_moon_id_key UNIQUE (moon_id);


--
-- Name: moon moon_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.moon
    ADD CONSTRAINT moon_pkey PRIMARY KEY (moon_id);


--
-- Name: planet planet_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.planet
    ADD CONSTRAINT planet_pkey PRIMARY KEY (planet_id);


--
-- Name: planet planet_planet_id_key; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.planet
    ADD CONSTRAINT planet_planet_id_key UNIQUE (planet_id);


--
-- Name: star star_galaxy_id_key; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_galaxy_id_key UNIQUE (galaxy_id);


--
-- Name: star star_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_pkey PRIMARY KEY (star_id);


--
-- Name: star star_star_id_key; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_star_id_key UNIQUE (star_id);


--
-- Name: moon moon_planet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.moon
    ADD CONSTRAINT moon_planet_id_fkey FOREIGN KEY (planet_id) REFERENCES public.planet(planet_id);


--
-- Name: planet planet_star_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.planet
    ADD CONSTRAINT planet_star_id_fkey FOREIGN KEY (star_id) REFERENCES public.star(star_id);


--
-- Name: star star_galaxy_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_galaxy_id_fkey FOREIGN KEY (galaxy_id) REFERENCES public.galaxy(galaxy_id);


--
-- PostgreSQL database dump complete
--

