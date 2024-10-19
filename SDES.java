import java.io.DataInputStream;

public class SDES {

    public int key1, key2;


    public static final int P10[] = { 3, 5, 2, 7, 4, 10, 1, 9, 8, 6 };  
    public static final int P8[] = { 6, 3, 7, 4, 8, 5, 10, 9 };
    public static final int P4[] = { 2, 4, 3, 1 };
    public static final int IP[] = { 2, 6, 3, 1, 4, 8, 5, 7 };
    public static final int IPI[] = { 4, 1, 3, 5, 7, 2, 8, 6 };
    public static final int EP[] = { 4, 1, 2, 3, 2, 3, 4, 1 };
    public static final int S0[][] = {
        { 1, 0, 3, 2 },
        { 3, 2, 1, 0 },
        { 0, 2, 1, 3 },
        { 3, 1, 3, 2 }
    };
    public static final int S1[][] = {
        { 0, 1, 2, 3 },
        { 2, 0, 1, 3 },
        { 3, 0, 1, 2 },
        { 2, 1, 0, 3 }
    };


    public static int permute(int input, int permutation[], int maxBits) {
        int output = 0;
        for (int i = 0; i < permutation.length; i++) {
            output = output << 1;
            output = output | (input >> (maxBits - permutation[i]) & 1);
        }
        return output;
    }


    public static int functionF(int right, int key) {
        int temp = permute(right, EP, 4) ^ key;
        int leftNibble = (temp >> 4) & 0xF;
        int rightNibble = temp & 0xF;
        leftNibble = S0[((leftNibble & 0x8) >> 2) | (leftNibble & 1)][(leftNibble >> 1) & 0x3];
        rightNibble = S1[((rightNibble & 0x8) >> 2) | (rightNibble & 1)][(rightNibble >> 1) & 0x3];
        temp = permute((leftNibble << 2) | rightNibble, P4, 4);
        return temp;
    }


    public static int functionFK(int message, int key) {
        int left = (message >> 4) & 0xF;
        int right = message & 0xF;
        return ((left ^ functionF(right, key)) << 4) | right;
    }


    public static int swap(int input) {
        return ((input & 0xF) << 4) | ((input >> 4) & 0xF);
    }


    public byte encrypt(int message) {
        message = permute(message, IP, 8);
        message = functionFK(message, key1);
        message = swap(message);
        message = functionFK(message, key2);
        message = permute(message, IPI, 8);
        return (byte) message;
    }


    public byte decrypt(int message) {
        message = permute(message, IP, 8);
        message = functionFK(message, key2);
        message = swap(message);
        message = functionFK(message, key1);
        message = permute(message, IPI, 8);
        return (byte) message;
    }


    public static void printBinary(int value, int bits) {
        int mask = 1 << (bits - 1);
        while (mask > 0) {
            System.out.print(((value & mask) == 0) ? '0' : '1');
            mask >>= 1;
        }
    }


    public SDES(int key) {
        key = permute(key, P10, 10);
        int leftHalf = (key >> 5) & 0x1F;
        int rightHalf = key & 0x1F;
        leftHalf = ((leftHalf & 0xF) << 1) | ((leftHalf & 0x10) >> 4);
        rightHalf = ((rightHalf & 0xF) << 1) | ((rightHalf & 0x10) >> 4);
        key1 = permute((leftHalf << 5) | rightHalf, P8, 10);
        leftHalf = ((leftHalf & 0x7) << 2) | ((leftHalf & 0x18) >> 3);
        rightHalf = ((rightHalf & 0x7) << 2) | ((rightHalf & 0x18) >> 3);
        key2 = permute((leftHalf << 5) | rightHalf, P8, 10);
    }


    public static void main(String args[]) throws Exception {
        DataInputStream input = new DataInputStream(System.in);
        System.out.println("Enter the 10 Bit Key- ");
        @SuppressWarnings("deprecation")
        int key = Integer.parseInt(input.readLine(), 2);
        SDES sdes = new SDES(key);
        System.out.println("Enter the 8 Bit message- ");
        @SuppressWarnings("deprecation")
        int message = Integer.parseInt(input.readLine(), 2);


        message = sdes.encrypt(message);
        System.out.print("\nEncrypted Message- ");
        printBinary(message, 8);

        message = sdes.decrypt(message);
        System.out.print("\nDecrypted Message- ");
        printBinary(message, 8);
    }
}
