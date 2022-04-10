query = {
    'checkIfIdExists' : '''
                        SELECT visitor_id
                        FROM userstats
                        WHERE visitor_id = %s;
                    ''', 
    'getCurrentStats': '''
                            SELECT games_played, games_won
                            FROM userstats
                            WHERE visitor_id = %s
                        ''',
    'createUser': '''
                    INSERT INTO userstats (visitor_id)
                    VALUES (%s);
                ''',
    'updateStatsIfCorrect': '''
                    UPDATE userstats
                    SET games_played = games_played + 1,
                        games_won = games_won + 1
                    WHERE visitor_id = %s;
                    ''',
    'updateStatsIfIncorrect': '''
                                UPDATE userstats
                                SET games_played = games_played + 1
                                WHERE visitor_id = %s;
                            ''',
    'showGlobalStats': '''
                            SELECT games_played, games_won
                            FROM userstats;
                        ''',
}
