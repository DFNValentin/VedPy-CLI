const sqlite = require("sqlite3");

const connectionDB = await sqlite.open({
    filename: "horcrux.db",
    driver: sqlite.Database,
});

const rows = await db.all("SELECT * FROM personal_data");
