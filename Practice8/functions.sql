CREATE OR REPLACE FUNCTION find_contacts(search_pattern TEXT)
RETURNS TABLE (id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.phone 
    FROM phonebook p
    WHERE p.name ILIKE '%' || search_pattern || '%'
       OR p.phone LIKE '%' || search_pattern || '%';
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION get_phonebook_paged(p_limit INT, p_offset INT)
RETURNS SETOF public.phonebook AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM public.phonebook
    ORDER BY id ASC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;