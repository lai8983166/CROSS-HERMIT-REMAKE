
void FUN__text__004c21f0(uint param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_14c [16];
  undefined4 local_10c;
  undefined1 local_108 [252];
  int local_c;
  int local_8;
  
  puVar2 = local_14c;
  for (iVar1 = 0x52; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_c = param_2;
  local_10c = FUN__text__004c2190(param_1 & 0xffff,*(undefined2 *)(param_2 + 4));
  FUN__text__004cd7b0(local_10c,local_108);
  FUN__text__004ce6e0(local_108,param_1);
  FUN__text__0042b2d0("[ Script File Read ] --> [ %s ] \n",local_108);
  *(undefined2 *)(local_8 + 0x24 + param_1 * 0x1c8) = 0;
  local_8 = 0x4c22a3;
  FUN__text__0056ce80();
  return;
}

