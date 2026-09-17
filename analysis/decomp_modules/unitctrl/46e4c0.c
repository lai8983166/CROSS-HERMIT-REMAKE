
void FUN__text__0046e4c0(undefined2 param_1,undefined2 param_2,int param_3)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [16];
  undefined4 local_8;
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  FUN__text__00472f40(CONCAT22((short)((uint)(param_3 / 0x3c) >> 0x10),param_1),
                      CONCAT22((short)((uint)(param_3 % 0x3c) >> 0x10),param_2),500,param_3 / 0x3c,1
                      ,0,0xffffffff,1);
  local_8 = 0x46e515;
  FUN__text__0056ce80();
  return;
}

