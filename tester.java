public class tester {
    public static void main(String[] args){
        persegi Persegi = new persegi();
        Persegi.sisi = 10;
        System.out.println("Keliling persegi = " + Persegi.hitungKeliling());
        System.out.println("laus Persegi = " + Persegi.hitungLuas());

        persegipanjang Persegiaja = new persegipanjang();
        Persegiaja.lebar = 4;
        Persegiaja.panjang = 5;
        System.out.println("keliling persegipanjang = " + Persegiaja.hitungKeliling());
        System.out.println("Luas persegipanjang = " + Persegiaja.hitungLuas());
    }
}
