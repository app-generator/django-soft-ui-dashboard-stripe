fetch("/ecommerce/config/")
.then((result) => {
  return result.json();
})
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);
  document.querySelector("#submitBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/ecommerce/create-checkout-session/?product=1&quantity=2")
    .then((result) => {
      return result.json();
    })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});