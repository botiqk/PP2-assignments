-- добавка или обновка
CREATE OR REPLACE PROCEDURE upsert_contact(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO public.phonebook (name, phone)
    VALUES (p_name, p_phone)
    ON CONFLICT (name) 
    DO UPDATE SET phone = EXCLUDED.phone;
END;
$$;


-- удаление
CREATE OR REPLACE PROCEDURE delete_contact_by_name_or_phone(p_value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value
       OR phone = p_value;
END;
$$;
