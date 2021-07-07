# Database "focus" 생성
create database focus

# 만든 Database 선택
\c focus

#수업의 고유번호 생성
create sequence 'class_id' start 1;
#유저 수업별 점수의 고유 번호 생성
create sequence 'score_id' start 1;

# Userinfo 테이블 생성
create table USERINFO(
    UserId character(12) primary key,
    UserName character varying(10) not null,
    UserPassword character varying(24) not null,
    IsProf boolean not null,
    UserEmail character varying(24) UNIQUE
);

# class 테이블 생성 (수업 관련 내용)
create table class (
    classid integer primary key,
    generatorid character varying(10) constraint userid references userinfo,
    classname character varying(24) unique not null,
    isOpen boolean
);

# user_class_rel 테이블 생성 (유저의 수업별, 그냥 점수 기록)
create table user_class_rel(
    id integer primary key,
    userid character(10) constraint userid references userinfo,
    classid integer constraint classid references class,
    score bigint not null,
    createdAt date not null
);


#  user_class_avg 테이블 생성 (수업의 평균 점수 저장)
create table user_class_avg(
    id character(10) primary key,
    userid character(10) constraint userid references userinfo,
    classid character(10) constraint classid references class,
    avg bigint not null,
    when_gen character varying(10) not null
);