const express = require('express');
const bodyParser = require('body-parser');
const neo4j = require('neo4j-driver');
const app = express();
const port = 3000; // Modifiez le port selon vos besoins

const uri = 'neo4j://<host>:<port>';
const user = '<username>';
const password = '<password>';
const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));

app.use(bodyParser.json());

async function findClosestBikeParks(lat, lon) {
    const session = driver.session();
    try {
        const result = await session.run(
            'MATCH (p:BikePark) \
            RETURN p, distance(point({latitude: $lat, longitude: $lon}), p.location) AS dist \
            ORDER BY dist ASC \
            LIMIT 5',
            { lat, lon }
        );
        return result.records.map(record => ({
            id: record.get('p').identity.low,
            name: record.get('p').properties.name,
            distance: record.get('dist')
        }));
    } finally {
        await session.close();
    }
}

app.post('/api/parking/search', async (req, res) => {
    const { lat, lon } = req.body;
    try {
        const parks = await findClosestBikeParks(lat, lon);
        res.json(parks);
    } catch (error) {
        console.error("Erreur lors de la recherche des parkings à vélo :", error);
        res.status(500).send("Erreur interne du serveur");
    }
});

app.listen(port, () => {
    console.log(`Serveur écoutant sur le port ${port}`);
});
