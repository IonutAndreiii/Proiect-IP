package com.gat.intelibar;

import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.ListView;

import androidx.appcompat.app.AppCompatActivity;

import java.text.DateFormatSymbols;
import java.util.ArrayList;

public class UserReportActivity extends AppCompatActivity {
    private Button btnBack;
    private ListView listView;
    private ArrayList<UserReport> report = new ArrayList<>();
    private ArrayList<String> reportInfo = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstance) {
        super.onCreate(savedInstance);
        setContentView(R.layout.activity_user_report);
        btnBack = (Button) findViewById(R.id.btnBack);
        btnBack.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        ListView listView = (ListView)findViewById(R.id.report_lisView);

        PopulateData("TM-11-79","30-05-2020", "09:58", "18:00");
        PopulateData("TM-11-79","30-05-2020", "09:58", "18:00");
        PopulateData("TM-11-79","30-05-2020", "09:58", "18:00");
        PopulateData("TM-11-79","30-05-2020", "09:58", "18:00");
        PopulateData("TM-11-79","30-05-2020", "09:58", "18:00");
        PopulateData("TM-11-79","30-05-2020", "09:58", "18:00");
        PopulateData("TM-11-79","30-05-2020", "09:58", "18:00");

        ArrayAdapter<String> reportAdapter = new ArrayAdapter<String>(this, R.layout.reporttextview, reportInfo);
        listView.setAdapter(reportAdapter);
    }

    public void PopulateData(String marca, String data, String ora_intrare, String ora_iesire) {

        UserReport info = new UserReport(marca,data, ora_intrare, ora_iesire);
        report.add(info);
        reportInfo.add(info.toString(Integer.toString(info.getIndex()), info.getMarca(),info.getData(),info.getOra_intrare(),info.getOra_iesire()));
    }

}
