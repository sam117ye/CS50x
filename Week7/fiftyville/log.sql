-- Keep a log of any SQL queries you execute as you solve the mystery.

-- read description
select description from crime_scene_reports;
where year = 2023 and month = 7 and day = 28 and street = "Humphery Street";

-- check for transcripts
select transcript from interviews
where year = 2023 and month = 7 and day = 28;

-- check for licence plate and get name
select name from people
join bakery_security_logs on bakery_security_logs.license_plate = people.license_plate
where year = 2023 and month = 7 and day = 28 and hour = 10 and minute >= 15 and minute <= 25
and activity = "exit";

-- check into atm

select name from people
join bank_accounts on bank_accounts.person_id = people.id
join atm_transactions on atm_transactions.account_number = bank_accounts.account_number
where year = 2023 and month = 7 and day = 28 and atm_location = "Leggett Street" and transaction_type = "withdraw";

-- check into flight and passengers

select name from people
join passengers on passengers.passport_number = people.passport_number
where passengers.flight_id = (
select id from flights
where year = 2023 and month = 7 and day = 29 and origin_airport_id =(
select id from airports where city = "Fiftyville" )
order by hour, minute
limit 1);

--check into calls
select name from people
join phone_calls on phone_calls.caller = people.phone_number
where year = 2023 and month = 7 and day = 28 and duration <= 60;


--where did they go to

select city from airports
where id = (
select destination_airport_id from flights
where year = 2023 and month = 7 and day = 29 and origin_airport_id =(
select id from airports where city = "Fiftyville" )
order by hour, minute
limit 1);

-- who is the accomplice
select name from people
join phone_calls on people.phone_number = phone_calls.receiver
where year = 2023 and month = 7 and day = 28 and duration <= 60 and caller = (
select phone_number from people
where name = "Bruce");



