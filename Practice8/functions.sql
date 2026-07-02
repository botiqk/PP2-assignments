-- поиск по шаблону (имя или телефон)
CREATE OR REPLACE FUNCTION find_contacts(search_pattern TEXT)
RETURNS TABLE (id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.phone 
    FROM phonebook p
    WHERE p.name ILIKE '%' || search_pattern || '%'
       OR p.phone ILIKE '%' || search_pattern || '%';
END;
$$ LANGUAGE plpgsql;


-- вывод контактов по частям (LIMIT и OFFSET)
CREATE OR REPLACE FUNCTION get_phonebook_paged(p_limit INT, p_offset INT)
RETURNS SETOF public.phonebook AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM public.phonebook
    ORDER BY id ASC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;


-- обработка несколько контактов, проверяем их и сохраняем только правильные
CREATE OR REPLACE FUNCTION bulk_insert_contacts(names TEXT[], phones TEXT[])
RETURNS TABLE (rejected_name TEXT, rejected_phone TEXT) AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        -- проверка правильности 
        IF phones[i] ~ '^\+?[0-9]{10,15}$' THEN
            INSERT INTO public.phonebook (name, phone) 
            VALUES (names[i], phones[i])
            ON CONFLICT (name) DO UPDATE SET phone = EXCLUDED.phone;
        ELSE
            rejected_name := names[i];
            rejected_phone := phones[i];
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
