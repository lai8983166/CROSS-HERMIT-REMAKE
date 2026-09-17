
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

uint __fastcall FUN__text__0054691a(float *param_1)

{
  float local_1c;
  float local_18;
  float local_14;
  
  if (_DAT_005d0a54 <= *param_1) {
    if (_DAT_005d0a40 < *param_1) {
      local_1c = 1.0;
    }
    else {
      local_1c = *param_1;
    }
  }
  else {
    local_1c = 0.0;
  }
  if (_DAT_005d0a54 <= param_1[1]) {
    if (_DAT_005d0a40 < param_1[1]) {
      local_18 = 1.0;
    }
    else {
      local_18 = param_1[1];
    }
  }
  else {
    local_18 = 0.0;
  }
  if (_DAT_005d0a54 <= param_1[2]) {
    if (param_1[2] <= _DAT_005d0a40) {
      local_14 = param_1[2];
    }
    else {
      local_14 = 1.0;
    }
  }
  else {
    local_14 = 0.0;
  }
  FUN__text__005468d8();
  return ((int)ROUND(local_1c * _DAT_005d0e40 + _DAT_005d0a3c) << 6 |
         (int)ROUND(local_18 * _DAT_005d0e3c + _DAT_005d0a3c)) << 5 |
         (int)ROUND(local_14 * _DAT_005d0e40 + _DAT_005d0a3c);
}

