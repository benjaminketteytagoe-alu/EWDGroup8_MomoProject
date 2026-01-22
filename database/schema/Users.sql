create table momo_erd.Users
(
    user_id        int auto_increment
        primary key,
    full_name      varchar(100)                                                     not null,
    phone_number   varchar(15)                                                      null,
    momo_pin       varchar(255)                                                     not null,
    account_status enum ('Active', 'Suspended', 'Closed') default 'Active'          null,
    created_at     timestamp                              default CURRENT_TIMESTAMP null,
    updated_at     timestamp                              default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    constraint phone_number
        unique (phone_number)
);

create index idx_account_status
    on momo_erd.Users (account_status);

create index idx_phone_number
    on momo_erd.Users (phone_number);

