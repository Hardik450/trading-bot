# Trading Bot Flow Diagrams

## 1. Order Placement Flow

```
┌─────────────────────────────────────────────────────────────┐
│ USER INITIATES ORDER                                         │
│ Command: python main.py order BTCUSDT BUY MARKET 0.001     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ CLI LAYER (main.py)                                         │
│ • Parse command line arguments                              │
│ • Validate input format                                     │
│ • Check configuration                                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ DATA MODEL (models.py)                                      │
│ • Create OrderRequest object                                │
│ • Validate all fields                                       │
│ • Ensure price present for LIMIT                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ SERVICE LAYER (order_service.py)                           │
│ • Validate symbol exists                                    │
│ • Log order request summary                                 │
│ • Call client to place order                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ CLIENT LAYER (binance_client.py)                           │
│ • Add timestamp to parameters                               │
│ • Generate HMAC SHA256 signature                           │
│ • Create authenticated request                             │
│ • Send POST to /fapi/v1/order                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ BINANCE API                                                 │
│ • Validate signature                                        │
│ • Check balance                                             │
│ • Execute order                                             │
│ • Return order details                                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE PROCESSING                                         │
│ • Parse JSON response                                       │
│ • Create OrderResponse model                                │
│ • Log execution details                                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ CLI OUTPUT                                                  │
│ • Display success message                                   │
│ • Show order details in table                              │
│ • Show order ID, status, price                             │
└─────────────────────────────────────────────────────────────┘
```

## 2. Error Handling Flow

```
┌─────────────────────────────────────────────────────────────┐
│ ERROR OCCURS                                                │
└────────────────────────┬────────────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │Validation│  │ Network  │  │   API    │
    │  Error   │  │  Error   │  │  Error   │
    └────┬─────┘  └────┬─────┘  └────┬─────┘
         │             │             │
         └─────────────┼─────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │ EXCEPTION CAUGHT        │
         │ • Log error details     │
         │ • Extract error message │
         │ • Determine error type  │
         └──────────┬──────────────┘
                    │
                    ▼
         ┌─────────────────────────┐
         │ USER-FRIENDLY OUTPUT    │
         │ • Show error type       │
         │ • Show error message    │
         │ • Suggest solution      │
         │ • Exit with error code  │
         └─────────────────────────┘
```

## 3. Application Startup Flow

```
┌─────────────────────────────────────────────────────────────┐
│ USER RUNS: python main.py order BTCUSDT BUY MARKET 0.001  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────┐
         │ Import Modules            │
         │ • config                  │
         │ • logger                  │
         │ • models                  │
         │ • binance_client          │
         │ • order_service           │
         └──────────┬────────────────┘
                    │
                    ▼
         ┌───────────────────────────┐
         │ Load Configuration        │
         │ • Read .env file          │
         │ • Load API credentials    │
         │ • Set base URL            │
         └──────────┬────────────────┘
                    │
                    ▼
         ┌───────────────────────────┐
         │ Setup Logger              │
         │ • Create log file handler │
         │ • Create console handler  │
         │ • Set log format          │
         └──────────┬────────────────┘
                    │
                    ▼
         ┌───────────────────────────┐
         │ Validate Configuration    │
         │ • Check API key exists    │
         │ • Check API secret exists │
         │ • Validate not default    │
         └──────────┬────────────────┘
                    │
         ┌──────────┴─────────┐
         │                    │
    Pass │               Fail │
         ▼                    ▼
    ┌─────────┐      ┌──────────────┐
    │Continue │      │Show Error &  │
    │         │      │Exit          │
    └────┬────┘      └──────────────┘
         │
         ▼
    ┌─────────────────────────────┐
    │ Parse CLI Arguments         │
    │ • Extract command           │
    │ • Extract parameters        │
    └──────────┬──────────────────┘
               │
               ▼
    ┌─────────────────────────────┐
    │ Execute Command             │
    │ • order                     │
    │ • balance                   │
    │ • positions                 │
    │ • test                      │
    └─────────────────────────────┘
```

## 4. Authentication Flow

```
┌─────────────────────────────────────────────────────────────┐
│ API Request Needs to be Made                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────┐
         │ Prepare Parameters        │
         │ {                         │
         │   symbol: "BTCUSDT",      │
         │   side: "BUY",            │
         │   type: "MARKET",         │
         │   quantity: 0.001         │
         │ }                         │
         └──────────┬────────────────┘
                    │
                    ▼
         ┌───────────────────────────┐
         │ Add Timestamp             │
         │ timestamp: 1707049247123  │
         └──────────┬────────────────┘
                    │
                    ▼
         ┌───────────────────────────┐
         │ Create Query String       │
         │ "symbol=BTCUSDT&side=BUY  │
         │  &type=MARKET&quantity=   │
         │  0.001&timestamp=..."     │
         └──────────┬────────────────┘
                    │
                    ▼
         ┌───────────────────────────┐
         │ Generate Signature        │
         │ HMAC SHA256 with secret   │
         │ signature = hmac(...)     │
         └──────────┬────────────────┘
                    │
                    ▼
         ┌───────────────────────────┐
         │ Add to Parameters         │
         │ signature: "abc123..."    │
         └──────────┬────────────────┘
                    │
                    ▼
         ┌───────────────────────────┐
         │ Add API Key Header        │
         │ X-MBX-APIKEY: "your_key"  │
         └──────────┬────────────────┘
                    │
                    ▼
         ┌───────────────────────────┐
         │ Send HTTPS Request        │
         │ POST to Binance API       │
         └──────────┬────────────────┘
                    │
                    ▼
         ┌───────────────────────────┐
         │ Receive Response          │
         │ JSON with order details   │
         └───────────────────────────┘
```

## 5. Component Interaction Diagram

```
┌──────────────┐
│   User/CLI   │
└──────┬───────┘
       │
       │ commands
       │
       ▼
┌──────────────────────────────────────────────────────┐
│                    main.py                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │   order    │  │  balance   │  │ positions  │   │
│  │  command   │  │  command   │  │  command   │   │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘   │
└────────┼───────────────┼───────────────┼───────────┘
         │               │               │
         │               │               │
         └───────┬───────┴───────┬───────┘
                 │               │
                 ▼               ▼
         ┌────────────────────────────────┐
         │     order_service.py           │
         │  ┌──────────────────────────┐  │
         │  │ • place_order()          │  │
         │  │ • get_account_balance()  │  │
         │  │ • get_positions()        │  │
         │  │ • validate_symbol()      │  │
         │  └────────┬─────────────────┘  │
         └───────────┼────────────────────┘
                     │
                     │
                     ▼
         ┌────────────────────────────────┐
         │    binance_client.py           │
         │  ┌──────────────────────────┐  │
         │  │ • place_order()          │  │
         │  │ • get_account_info()     │  │
         │  │ • get_position_info()    │  │
         │  │ • _send_signed_request() │  │
         │  │ • _generate_signature()  │  │
         │  └────────┬─────────────────┘  │
         └───────────┼────────────────────┘
                     │
                     │ HTTPS
                     │
                     ▼
         ┌────────────────────────────────┐
         │      Binance API               │
         │  testnet.binancefuture.com     │
         └────────────────────────────────┘

Supporting Components (used by all layers):

┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│  config.py  │  │  logger.py   │  │  models.py   │
│             │  │              │  │              │
│ • API key   │  │ • File log   │  │ • OrderReq   │
│ • Secret    │  │ • Console    │  │ • OrderResp  │
│ • Base URL  │  │ • Format     │  │ • Validation │
└─────────────┘  └──────────────┘  └──────────────┘

         ┌──────────────┐
         │exceptions.py │
         │              │
         │ • Custom     │
         │   Exceptions │
         └──────────────┘
```

## 6. Data Validation Flow

```
User Input
    │
    ▼
┌─────────────────────┐
│ CLI Parsing         │
│ • argparse/typer    │
│ • Basic type check  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Pydantic Model      │
│ OrderRequest        │
│                     │
│ ✓ symbol: str       │
│   └─ uppercase      │
│   └─ no spaces      │
│                     │
│ ✓ side: OrderSide   │
│   └─ BUY or SELL    │
│                     │
│ ✓ type: OrderType   │
│   └─ MARKET/LIMIT   │
│                     │
│ ✓ quantity: float   │
│   └─ > 0            │
│                     │
│ ✓ price: Optional   │
│   └─ required if    │
│      LIMIT          │
│   └─ > 0            │
└──────┬──────────────┘
       │
       ▼ Valid?
┌──────┴──────┐
│      Yes    │ No
│      │      └─────► ValidationError
│      ▼                    │
│  Continue                 │
│      │                    │
│      ▼                    ▼
│  Service              Show Error
│   Layer               & Exit
```

## 7. Logging Flow

```
┌──────────────────────────────────────┐
│ Any Operation in Application         │
└────────────┬─────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────┐  ┌──────────┐
│ Info     │  │ Error    │
│ Messages │  │ Messages │
└─────┬────┘  └─────┬────┘
      │             │
      └──────┬──────┘
             │
             ▼
    ┌─────────────────┐
    │ Logger Module   │
    │                 │
    │ Format:         │
    │ timestamp       │
    │ - module        │
    │ - level         │
    │ - message       │
    └────┬───────┬────┘
         │       │
    File │       │ Console
         │       │
         ▼       ▼
┌──────────┐ ┌─────────┐
│ .log     │ │ stdout  │
│ file     │ │         │
│          │ │ INFO+   │
│ DEBUG+   │ │ only    │
└──────────┘ └─────────┘
```

## 8. Success vs Failure Paths

```
                    Order Request
                          │
                          ▼
                    ┌───────────┐
                    │ Validate  │
                    │ Config    │
                    └─────┬─────┘
                          │
                ┌─────────┴─────────┐
                │                   │
             Valid              Invalid
                │                   │
                ▼                   ▼
          ┌──────────┐      ┌──────────┐
          │ Create   │      │  Exit    │
          │ Request  │      │  Error   │
          └────┬─────┘      └──────────┘
               │
               ▼
          ┌──────────┐
          │ Validate │
          │ Inputs   │
          └────┬─────┘
               │
     ┌─────────┴─────────┐
     │                   │
  Valid              Invalid
     │                   │
     ▼                   ▼
┌──────────┐      ┌──────────┐
│ Call API │      │  Show    │
│          │      │  Error   │
└────┬─────┘      └──────────┘
     │
     ▼
┌──────────┐
│ Network  │
│ Request  │
└────┬─────┘
     │
┌────┴────┐
│         │
Success   Fail
│         │
▼         ▼
┌───────────┐  ┌───────────┐
│ Parse     │  │ Handle    │
│ Response  │  │ Error     │
│           │  │ • Log     │
│ Display   │  │ • Show    │
│ Success   │  │ • Suggest │
└───────────┘  └───────────┘
```

These diagrams show the complete flow of data and control through the trading bot application, from user input to API response and error handling.
