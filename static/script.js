$(document).ready(function () {
  function updateTable(data) {
    let table = $("#resultTable");
    table.empty();
    data.forEach((item, index) => {
      table.append(`
                <tr>
                    <td>${item.hasil_ubinan}</td>
                    <td>${item.luas_lahan}</td>
                    <td>${item.gkp_per_ha}</td>
                    <td>${item.gkg_per_ha}</td>
                    <td>${item.gkg_per_plot}</td>
                    <td>${item.ton_gkp}</td>
                    <td>${item.ton_gkg}</td>
                    <td>${item.ton_beras}</td>
                    <td><button class="hapus" data-index="${index}">Hapus</button></td>
                </tr>
            `);
    });
  }

  $("#hitung").click(function () {
    let hasilUbinan = $("#hasil_ubinan").val();
    let luasLahan = $("#luas_lahan").val();

    if (hasilUbinan && luasLahan) {
      $.post(
        "/convert",
        { hasil_ubinan: hasilUbinan, luas_lahan: luasLahan },
        function (data) {
          updateTable(data);
        }
      );
    } else {
      alert("Masukkan nilai yang valid!");
    }
  });

  $(document).on("click", ".hapus", function () {
    let index = $(this).data("index");
    $.post("/delete", { index: index }, function (data) {
      updateTable(data);
    });
  });

  $("#downloadExcel").click(function () {
    window.location.href = "/download";
  });
});
