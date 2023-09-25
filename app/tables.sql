CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT uuid_generate_v4() NOT NULL,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    created_at TIMESTAMP with time zone DEFAULT now() NOT NULL,
    updated_at TIMESTAMP with time zone DEFAULT now() ON UPDATE now() NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS tasks (
    id UUID DEFAULT uuid_generate_v4() NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR,
    done BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP with time zone DEFAULT now() NOT NULL,
    updated_at TIMESTAMP with time zone DEFAULT now() ON UPDATE now() NOT NULL,
    user_id UUID NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);