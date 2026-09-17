
undefined4 FUN__text__00417a70(undefined4 param_1,undefined4 param_2,char *param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_44c [16];
  int local_40c;
  uint local_408 [257];
  
  puVar2 = local_44c;
  for (iVar1 = 0x112; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  for (local_40c = 1; local_40c != 0x100; local_40c = local_40c + 1) {
    if (((param_3[2] == param_3[local_40c * 4 + 2]) && (param_3[1] == param_3[local_40c * 4 + 1]))
       && (*param_3 == param_3[local_40c * 4])) {
      local_408[local_40c] = 0;
    }
    else {
      local_408[local_40c] =
           (uint)CONCAT12(param_3[local_40c * 4],
                          CONCAT11(param_3[local_40c * 4 + 1],param_3[local_40c * 4 + 2]));
    }
  }
  return 0;
}

