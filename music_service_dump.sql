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
-- Структура таблицы users
--

CREATE TABLE public.users (
    user_id uuid DEFAULT gen_random_uuid() NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    username character varying(100),
    registration_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    subscription_type character varying(20) DEFAULT 'free'::character varying,
    subscription_expiry date,
    country_code character(2)
);

--
-- Данные для таблицы users
--

INSERT INTO public.users VALUES 
('11111111-1111-1111-1111-111111111111', 'user1@example.com', 'hash1', 'User1', '2024-01-15 10:00:00', 'premium', '2024-02-15', 'RU'),
('22222222-2222-2222-2222-222222222222', 'user2@example.com', 'hash2', 'User2', '2024-01-15 10:05:00', 'free', NULL, 'RU'),
('33333333-3333-3333-3333-333333333333', 'user3@example.com', 'hash3', 'User3', '2024-01-15 10:10:00', 'free', NULL, 'RU'),
('44444444-4444-4444-4444-444444444444', 'user4@example.com', 'hash4', 'User4', '2024-01-15 10:15:00', 'free', NULL, 'RU'),
('55555555-5555-5555-5555-555555555555', 'user5@example.com', 'hash5', 'User5', '2024-01-15 10:20:00', 'free', NULL, 'RU');

--
-- Структура таблицы subscription_plans
--

CREATE TABLE public.subscription_plans (
    plan_id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(50) NOT NULL,
    price numeric(10,2) NOT NULL,
    description text
);

--
-- Данные для таблицы subscription_plans
--

INSERT INTO public.subscription_plans VALUES 
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Free', 0.00, 'Бесплатный тариф с рекламой'),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Premium', 299.00, 'Премиум без рекламы, скачивание треков'),
('cccccccc-cccc-cccc-cccc-cccccccccccc', 'Family', 499.00, 'Семейная подписка для 6 человек');

--
-- Структура таблицы genres
--

CREATE TABLE public.genres (
    genre_id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(100) NOT NULL,
    description text
);

--
-- Данные для таблицы genres
--

INSERT INTO public.genres VALUES 
('aaaaaaaa-1111-1111-1111-aaaaaaaaaaaa', 'Pop', 'Поп-музыка'),
('bbbbbbbb-2222-2222-2222-bbbbbbbbbbbb', 'Rock', 'Рок-музыка'),
('cccccccc-3333-3333-3333-cccccccccccc', 'Hip-Hop', 'Хип-хоп и рэп'),
('dddddddd-4444-4444-4444-dddddddddddd', 'Electronic', 'Электронная музыка'),
('eeeeeeee-5555-5555-5555-eeeeeeeeeeee', 'Jazz', 'Джаз'),
('ffffffff-6666-6666-6666-ffffffffffff', 'Classical', 'Классическая музыка'),
('gggggggg-7777-7777-7777-gggggggggggg', 'Metal', 'Метал'),
('hhhhhhhh-8888-8888-8888-hhhhhhhhhhhh', 'Indie', 'Инди-музыка');

--
-- Структура таблицы artists
--

CREATE TABLE public.artists (
    artist_id uuid DEFAULT gen_random_uuid() NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    country_code character(2),
    date_formed date,
    photo_url character varying(500)
);

--
-- Данные для таблицы artists
--

INSERT INTO public.artists VALUES 
('a1111111-1111-1111-1111-111111111111', 'The Weeknd', 'Канадский певец', 'CA', '2010-01-01', NULL),
('a2222222-2222-2222-2222-222222222222', 'Imagine Dragons', 'Американская поп-рок группа', 'US', '2008-01-01', NULL),
('a3333333-3333-3333-3333-333333333333', 'Eminem', 'Американский рэпер', 'US', '1996-01-01', NULL),
('a4444444-4444-4444-4444-444444444444', 'Daft Punk', 'Французский электронный дуэт', 'FR', '1993-01-01', NULL),
('a5555555-5555-5555-5555-555555555555', 'Queen', 'Британская рок-группа', 'UK', '1970-01-01', NULL);

--
-- Структура таблицы artist_genres
--

CREATE TABLE public.artist_genres (
    artist_id uuid NOT NULL,
    genre_id uuid NOT NULL
);

--
-- Данные для таблицы artist_genres
--

INSERT INTO public.artist_genres VALUES 
('a1111111-1111-1111-1111-111111111111', 'aaaaaaaa-1111-1111-1111-aaaaaaaaaaaa'),
('a1111111-1111-1111-1111-111111111111', 'eeeeeeee-5555-5555-5555-eeeeeeeeeeee'),
('a2222222-2222-2222-2222-222222222222', 'aaaaaaaa-1111-1111-1111-aaaaaaaaaaaa'),
('a2222222-2222-2222-2222-222222222222', 'bbbbbbbb-2222-2222-2222-bbbbbbbbbbbb'),
('a2222222-2222-2222-2222-222222222222', 'hhhhhhhh-8888-8888-8888-hhhhhhhhhhhh'),
('a3333333-3333-3333-3333-333333333333', 'cccccccc-3333-3333-3333-cccccccccccc'),
('a4444444-4444-4444-4444-444444444444', 'dddddddd-4444-4444-4444-dddddddddddd'),
('a5555555-5555-5555-5555-555555555555', 'bbbbbbbb-2222-2222-2222-bbbbbbbbbbbb'),
('a5555555-5555-5555-5555-555555555555', 'aaaaaaaa-1111-1111-1111-aaaaaaaaaaaa');

--
-- Структура таблицы albums
--

CREATE TABLE public.albums (
    album_id uuid DEFAULT gen_random_uuid() NOT NULL,
    title character varying(255) NOT NULL,
    artist_id uuid NOT NULL,
    release_date date,
    cover_art_url character varying(500)
);

--
-- Данные для таблицы albums
--

INSERT INTO public.albums VALUES 
('al111111-1111-1111-1111-111111111111', 'After Hours', 'a1111111-1111-1111-1111-111111111111', '2020-03-20', NULL),
('al222222-2222-2222-2222-222222222222', 'Starboy', 'a1111111-1111-1111-1111-111111111111', '2016-11-25', NULL),
('al333333-3333-3333-3333-333333333333', 'Night Visions', 'a2222222-2222-2222-2222-222222222222', '2012-09-04', NULL),
('al444444-4444-4444-4444-444444444444', 'The Eminem Show', 'a3333333-3333-3333-3333-333333333333', '2002-05-26', NULL),
('al555555-5555-5555-5555-555555555555', 'Random Access Memories', 'a4444444-4444-4444-4444-444444444444', '2013-05-17', NULL),
('al666666-6666-6666-6666-666666666666', 'A Night at the Opera', 'a5555555-5555-5555-5555-555555555555', '1975-11-21', NULL);

--
-- Структура таблицы tracks
--

CREATE TABLE public.tracks (
    track_id uuid DEFAULT gen_random_uuid() NOT NULL,
    title character varying(255) NOT NULL,
    duration integer NOT NULL,
    file_url character varying(500) NOT NULL,
    album_id uuid,
    track_number integer,
    play_count bigint DEFAULT 0
);

--
-- Данные для таблицы tracks
--

INSERT INTO public.tracks VALUES 
('t1111111-1111-1111-1111-111111111111', 'Blinding Lights', 200, '/tracks/blinding_lights.mp3', 'al111111-1111-1111-1111-111111111111', 1, 150),
('t2222222-2222-2222-2222-222222222222', 'Save Your Tears', 215, '/tracks/save_your_tears.mp3', 'al111111-1111-1111-1111-111111111111', 2, 120),
('t3333333-3333-3333-3333-333333333333', 'Starboy', 230, '/tracks/starboy.mp3', 'al222222-2222-2222-2222-222222222222', 1, 180),
('t4444444-4444-4444-4444-444444444444', 'Radioactive', 187, '/tracks/radioactive.mp3', 'al333333-3333-3333-3333-333333333333', 1, 200),
('t5555555-5555-5555-5555-555555555555', 'Demons', 177, '/tracks/demons.mp3', 'al333333-3333-3333-3333-333333333333', 2, 160),
('t6666666-6666-6666-6666-666666666666', 'Without Me', 290, '/tracks/without_me.mp3', 'al444444-4444-4444-4444-444444444444', 1, 220),
('t7777777-7777-7777-7777-777777777777', 'Lose Yourself', 326, '/tracks/lose_yourself.mp3', NULL, NULL, 300),
('t8888888-8888-8888-8888-888888888888', 'Get Lucky', 369, '/tracks/get_lucky.mp3', 'al555555-5555-5555-5555-555555555555', 1, 140),
('t9999999-9999-9999-9999-999999999999', 'Bohemian Rhapsody', 354, '/tracks/bohemian_rhapsody.mp3', 'al666666-6666-6666-6666-666666666666', 1, 250),
('t0000000-0000-0000-0000-000000000000', 'We Will Rock You', 122, '/tracks/we_will_rock_you.mp3', 'al666666-6666-6666-6666-666666666666', 2, 190);

--
-- Структура таблицы playlists
--

CREATE TABLE public.playlists (
    playlist_id uuid DEFAULT gen_random_uuid() NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    is_public boolean DEFAULT false,
    created_by uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    cover_image_url character varying(500)
);

--
-- Данные для таблицы playlists
--

INSERT INTO public.playlists VALUES 
('p1111111-1111-1111-1111-111111111111', 'Мой топ 2024', 'Лучшие треки 2024 года', true, '11111111-1111-1111-1111-111111111111', '2024-01-15 10:30:00', NULL),
('p2222222-2222-2222-2222-222222222222', 'Для тренировки', 'Энергичная музыка для спорта', true, '22222222-2222-2222-2222-222222222222', '2024-01-15 10:35:00', NULL);

--
-- Структура таблицы playlist_tracks
--

CREATE TABLE public.playlist_tracks (
    playlist_id uuid NOT NULL,
    track_id uuid NOT NULL,
    added_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    added_by uuid NOT NULL
);

--
-- Данные для таблицы playlist_tracks
--

INSERT INTO public.playlist_tracks VALUES 
('p1111111-1111-1111-1111-111111111111', 't1111111-1111-1111-1111-111111111111', '2024-01-15 10:31:00', '11111111-1111-1111-1111-111111111111'),
('p1111111-1111-1111-1111-111111111111', 't2222222-2222-2222-2222-222222222222', '2024-01-15 10:32:00', '11111111-1111-1111-1111-111111111111'),
('p1111111-1111-1111-1111-111111111111', 't3333333-3333-3333-3333-333333333333', '2024-01-15 10:33:00', '11111111-1111-1111-1111-111111111111'),
('p2222222-2222-2222-2222-222222222222', 't4444444-4444-4444-4444-444444444444', '2024-01-15 10:36:00', '22222222-2222-2222-2222-222222222222'),
('p2222222-2222-2222-2222-222222222222', 't5555555-5555-5555-5555-555555555555', '2024-01-15 10:37:00', '22222222-2222-2222-2222-222222222222'),
('p2222222-2222-2222-2222-222222222222', 't6666666-6666-6666-6666-666666666666', '2024-01-15 10:38:00', '22222222-2222-2222-2222-222222222222');

--
-- Структура таблицы listening_history
--

CREATE TABLE public.listening_history (
    history_id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    track_id uuid NOT NULL,
    listened_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

--
-- Данные для таблицы listening_history (примеры)
--

INSERT INTO public.listening_history VALUES 
(gen_random_uuid(), '11111111-1111-1111-1111-111111111111', 't1111111-1111-1111-1111-111111111111', '2024-01-15 09:00:00'),
(gen_random_uuid(), '11111111-1111-1111-1111-111111111111', 't2222222-2222-2222-2222-222222222222', '2024-01-15 09:05:00'),
(gen_random_uuid(), '22222222-2222-2222-2222-222222222222', 't3333333-3333-3333-3333-333333333333', '2024-01-15 09:10:00'),
(gen_random_uuid(), '33333333-3333-3333-3333-333333333333', 't4444444-4444-4444-4444-444444444444', '2024-01-15 09:15:00');

--
-- Структура таблицы user_likes
--

CREATE TABLE public.user_likes (
    user_id uuid NOT NULL,
    track_id uuid NOT NULL,
    liked_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

--
-- Данные для таблицы user_likes
--

INSERT INTO public.user_likes VALUES 
('11111111-1111-1111-1111-111111111111', 't1111111-1111-1111-1111-111111111111', '2024-01-15 10:40:00'),
('22222222-2222-2222-2222-222222222222', 't2222222-2222-2222-2222-222222222222', '2024-01-15 10:41:00'),
('33333333-3333-3333-3333-333333333333', 't3333333-3333-3333-3333-333333333333', '2024-01-15 10:42:00'),
('11111111-1111-1111-1111-111111111111', 't4444444-4444-4444-4444-444444444444', '2024-01-15 10:43:00'),
('22222222-2222-2222-2222-222222222222', 't5555555-5555-5555-5555-555555555555', '2024-01-15 10:44:00'),
('33333333-3333-3333-3333-333333333333', 't6666666-6666-6666-6666-666666666666', '2024-01-15 10:45:00'),
('44444444-4444-4444-4444-444444444444', 't7777777-7777-7777-7777-777777777777', '2024-01-15 10:46:00');

--
-- Структура таблицы payments
--

CREATE TABLE public.payments (
    payment_id uuid DEFAULT gen_random_uuid() NOT NULL,
    user_id uuid NOT NULL,
    plan_id uuid NOT NULL,
    amount numeric(10,2) NOT NULL,
    payment_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(20) DEFAULT 'pending'::character varying,
    external_payment_id character varying(255)
);

--
-- Данные для таблицы payments
--

INSERT INTO public.payments VALUES 
('pay11111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 299.00, '2024-01-15 10:25:00', 'completed', 'ext_12345');

--
-- Индексы
--

ALTER TABLE ONLY public.artist_genres
    ADD CONSTRAINT artist_genres_pkey PRIMARY KEY (artist_id, genre_id);

ALTER TABLE ONLY public.playlist_tracks
    ADD CONSTRAINT playlist_tracks_pkey PRIMARY KEY (playlist_id, track_id);

ALTER TABLE ONLY public.user_likes
    ADD CONSTRAINT user_likes_pkey PRIMARY KEY (user_id, track_id);

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_pkey PRIMARY KEY (album_id);

ALTER TABLE ONLY public.artists
    ADD CONSTRAINT artists_pkey PRIMARY KEY (artist_id);

ALTER TABLE ONLY public.artist_genres
    ADD CONSTRAINT artist_genres_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES public.artists(artist_id);

ALTER TABLE ONLY public.artist_genres
    ADD CONSTRAINT artist_genres_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.genres(genre_id);

ALTER TABLE ONLY public.albums
    ADD CONSTRAINT albums_artist_id_fkey FOREIGN KEY (artist_id) REFERENCES public.artists(artist_id);

ALTER TABLE ONLY public.listening_history
    ADD CONSTRAINT listening_history_track_id_fkey FOREIGN KEY (track_id) REFERENCES public.tracks(track_id);

ALTER TABLE ONLY public.listening_history
    ADD CONSTRAINT listening_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_plan_id_fkey FOREIGN KEY (plan_id) REFERENCES public.subscription_plans(plan_id);

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE ONLY public.playlist_tracks
    ADD CONSTRAINT playlist_tracks_added_by_fkey FOREIGN KEY (added_by) REFERENCES public.users(user_id);

ALTER TABLE ONLY public.playlist_tracks
    ADD CONSTRAINT playlist_tracks_playlist_id_fkey FOREIGN KEY (playlist_id) REFERENCES public.playlists(playlist_id);

ALTER TABLE ONLY public.playlist_tracks
    ADD CONSTRAINT playlist_tracks_track_id_fkey FOREIGN KEY (track_id) REFERENCES public.tracks(track_id);

ALTER TABLE ONLY public.playlists
    ADD CONSTRAINT playlists_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.users(user_id);

ALTER TABLE ONLY public.subscription_plans
    ADD CONSTRAINT subscription_plans_pkey PRIMARY KEY (plan_id);

ALTER TABLE ONLY public.tracks
    ADD CONSTRAINT tracks_pkey PRIMARY KEY (track_id);

ALTER TABLE ONLY public.tracks
    ADD CONSTRAINT tracks_album_id_fkey FOREIGN KEY (album_id) REFERENCES public.albums(album_id);

ALTER TABLE ONLY public.user_likes
    ADD CONSTRAINT user_likes_track_id_fkey FOREIGN KEY (track_id) REFERENCES public.tracks(track_id);

ALTER TABLE ONLY public.user_likes
    ADD CONSTRAINT user_likes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);

ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_pkey PRIMARY KEY (genre_id);

ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_name_key UNIQUE (name);

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (payment_id);

CREATE INDEX idx_listening_history_user_listened ON public.listening_history USING btree (user_id, listened_at);

CREATE INDEX idx_tracks_play_count ON public.tracks USING btree (play_count DESC);

CREATE INDEX idx_users_email ON public.users USING btree (email);

