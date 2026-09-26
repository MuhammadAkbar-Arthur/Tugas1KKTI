class Enigma:
    def __init__(self):
        # Konfigurasi Rotor & Reflector M3
        self.rotors = {
            'I':   {'wire': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'notch': 'Q'},
            'II':  {'wire': 'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'notch': 'E'},
            'III': {'wire': 'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'notch': 'V'}
        }
        self.reflector = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'
        
        # Pengaturan khusus Anda
        self.order = ['I', 'II', 'III'] # Kiri ke Kanan
        self.rings = [6, 22, 24]        # G(6), W(22), Y(24) -- A=0
        self.pos = [9, 21, 15]          # J(9), V(21), P(15) -- A=0
        
        # Plugboard: B-Q, M-E
        self.plugboard = {}
        for pair in ["BQ", "ME"]:
            self.plugboard[pair[0]] = pair[1]
            self.plugboard[pair[1]] = pair[0]

    def step_rotors(self):
        # Logika stepping Enigma (termasuk double stepping)
        step_left = False
        step_middle = False
        step_right = True # Rotor kanan selalu berputar
        
        # Cek notch untuk rotor tengah dan kanan
        if chr(self.pos[1] + 65) == self.rotors[self.order[1]]['notch']:
            step_left = True
            step_middle = True
        if chr(self.pos[2] + 65) == self.rotors[self.order[2]]['notch']:
            step_middle = True

        if step_left:   self.pos[0] = (self.pos[0] + 1) % 26
        if step_middle: self.pos[1] = (self.pos[1] + 1) % 26
        if step_right:  self.pos[2] = (self.pos[2] + 1) % 26

    def process_letter(self, char):
        if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": return char
        self.step_rotors()
        
        # Melewati Plugboard
        c = self.plugboard.get(char, char)
        idx = ord(c) - 65
        
        # Forward Pass (Kanan ke Kiri)
        for i in range(2, -1, -1):
            offset = self.pos[i] - self.rings[i]
            core_in = (idx + offset) % 26
            wire_char = self.rotors[self.order[i]]['wire'][core_in]
            idx = (ord(wire_char) - 65 - offset) % 26
            
        # Melewati Reflector
        idx = (ord(self.reflector[idx]) - 65) % 26
        
        # Backward Pass (Kiri ke Kanan)
        for i in range(3):
            offset = self.pos[i] - self.rings[i]
            core_in_char = chr(((idx + offset) % 26) + 65)
            wire_idx = self.rotors[self.order[i]]['wire'].index(core_in_char)
            idx = (wire_idx - offset) % 26
            
        # Kembali melewati Plugboard
        c_out = chr(idx + 65)
        return self.plugboard.get(c_out, c_out)

    def decrypt(self, text):
        return ''.join([self.process_letter(c) for c in text])

# Ciphertext milik Anda
ciphertext = "EBMFZRVXWWKWBWSGEOBRNBORWXFXDNEYZOUORLNNGAOGE"

enigma = Enigma()
plaintext = enigma.decrypt(ciphertext)
print(f"Hasil Dekripsi Bagian 3:\n{plaintext}")