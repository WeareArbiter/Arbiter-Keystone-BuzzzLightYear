CREATE FUNCTION notify_projectstate() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    PERFORM pg_notify('projectstate', NEW.date, NEW.task_name, NEW.status, NEW.log, NEW.time);
    RETURN NULL;
END;
$$;

CREATE TRIGGER updated_projectstate_trigger AFTER INSERT ON tracker_projectstate
FOR EACH ROW EXECUTE PROCEDURE notify_projectstate();
