from dataclasses import dataclass


@dataclass
class VoucherProcessor:
    def _pre_process(self, df):
        return df

    def _transform(self, df):
        return df

    def process(self, raw_df):
        clean_df = self._pre_process(raw_df)
        transformed_df = self._transform(clean_df)
        return transformed_df
