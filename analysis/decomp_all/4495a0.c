
void __fastcall FUN__text__004495a0(int param_1)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 local_48 [16];
  int local_8;
  
  puVar3 = local_48;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  FUN__text__00449650(0,param_1 + 0x8a60);
  FUN__text__00449650(1,local_8 + 0x8a68);
  uVar4 = 0;
  uVar1 = FUN__text__0044bed0(0);
  FUN__text__004496d0(local_8 + 0x8a60,local_8 + 0x8a70,uVar1,uVar4);
  uVar4 = 0x40;
  uVar1 = FUN__text__0044bed0(1);
  FUN__text__004496d0(local_8 + 0x8a68,local_8 + 0x8a78,uVar1,uVar4);
  local_8 = 0x449644;
  FUN__text__0056ce80();
  return;
}

