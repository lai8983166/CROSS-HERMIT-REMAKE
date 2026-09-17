
void FUN__text1__00810f2b(undefined4 param_1,uint param_2,uint param_3)

{
  undefined4 local_8;
  
  for (local_8 = param_2;
      local_8 < param_2 + ((int)((param_3 & 0xfffffff8) + ((int)param_3 >> 0x1f & 3U)) >> 2) * 4;
      local_8 = local_8 + 8) {
    FUN__text1__00810f84(param_1,local_8,local_8 + 4);
  }
  return;
}

