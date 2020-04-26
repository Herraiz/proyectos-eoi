class Song:
    def __init__(self, track, artist, genre, bpm, energy, danceability, length):
        self.track = track
        self.artist = artist
        self.genre = genre
        self.bpm = bpm
        self.energy = energy
        self.danceability = danceability
        self.length = length

    def __str__(self):
        return f'{self.track},{self.artist},{self.genre},{self.bpm},{self.energy},{self.danceability},{self.length}'

    def change_speed(self, relative_bpm):
        self.bpm = self.bpm + relative_bpm
        self.energy = self.energy + 2 * relative_bpm
        self.danceability = self.danceability + 3 * relative_bpm
        self.length = self.length + (-1) * relative_bpm

    @staticmethod
    def load_songs(path):
        songs = []
        with open(path, 'r') as fin:
            for line in fin:
                data = line.strip().split(',')
                songs.append(Song(data[0], data[1], data[2], int(data[3]), int(data[4]), int(data[5]), int(data[6])))
        return songs

    @staticmethod
    def save_songs(songs, path):
        with open(path, 'w') as fout:
            for song in songs:
                fout.write(str(song) + "\n")