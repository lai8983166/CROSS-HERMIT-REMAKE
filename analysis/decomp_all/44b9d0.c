
void FUN__text__0044b9d0(int param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_50 [16];
  char *local_10;
  undefined4 local_c;
  undefined4 local_8;
  
  puVar2 = local_50;
  for (iVar1 = 0x13; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (param_1 != param_2) {
    local_c = FUN__text__0044c200(param_1);
    local_10 = (char *)FUN__text__0044c200(param_2);
    if (*local_10 == '\x01') {
      FUN__text__0044b950(1);
    }
  }
  local_8 = 0x44ba42;
  FUN__text__0056ce80();
  return;
}

