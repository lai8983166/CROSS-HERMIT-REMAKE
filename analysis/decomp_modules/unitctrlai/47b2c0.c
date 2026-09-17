
void FUN__text__0047b2c0(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = FUN__text__0047a8e0(param_1);
  if (*(char *)(local_c + 0x17) != '\0') {
    local_10 = FUN__text__0047b340(param_1,param_2,0,(int)*(char *)(local_c + 0x17),
                                   (int)*(char *)(local_c + 0x18));
  }
  local_8 = 0x47b330;
  FUN__text__0056ce80();
  return;
}

