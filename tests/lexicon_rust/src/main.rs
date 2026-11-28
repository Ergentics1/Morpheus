fn main() {
    match morpheus_lexicon_audit::verify_all_six_gates() {
        Ok(msg) => println!("[PASS] {}", msg),
        Err(err) => {
            eprintln!("[FAIL] {}", err);
            std::process::exit(1);
        }
    }
}
