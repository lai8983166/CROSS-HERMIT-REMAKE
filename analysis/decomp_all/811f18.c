
void FUN__text1__00811f18(uint param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  uint local_24;
  uint local_20;
  uint local_1c;
  uint local_18;
  uint local_14;
  uint local_10;
  uint local_c;
  uint local_8;
  
  local_8 = param_1;
  local_20 = param_1 >> 8 | param_1 << 0x18;
  local_1c = local_20 >> 8 | (param_1 >> 8) << 0x18;
  local_18 = local_1c >> 8 | (local_20 >> 8) << 0x18;
  local_24 = param_1;
  local_14 = local_18;
  local_10 = local_1c;
  local_c = local_20;
  FUN__text1__00811d10(&local_24,param_2,param_3,param_4);
  return;
}

